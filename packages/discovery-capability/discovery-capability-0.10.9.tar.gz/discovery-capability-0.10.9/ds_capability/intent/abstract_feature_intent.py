import pyarrow as pa
import pyarrow.compute as pc
from ds_core.intent.abstract_intent import AbstractIntentModel
from pyarrow.lib import ArrowNotImplementedError


class AbstractFeatureIntentModel(AbstractIntentModel):

    _INTENT_PARAMS = ['self', 'save_intent', 'intent_level', 'intent_order',
                      'replace_intent', 'remove_duplicates', 'seed']

    def run_intent_pipeline(self, canonical: pa.Table=None, intent_level: [str, int]=None, seed: int=None,
                            simulate: bool=None, **kwargs) -> pa.Table:
        """Collectively runs all parameterised intent taken from the property manager against the code base as
        defined by the intent_contract. The whole run can be seeded though any parameterised seeding in the intent
        contracts will take precedence

        :param canonical: a direct or generated pd.DataFrame. see context notes below
        :param intent_level: (optional) a single intent_level to run
        :param seed: (optional) a seed value that will be applied across the run: default to None
        :param simulate: (optional) returns a report of the order of run and return the indexed column order of run
        :return: a pa.Table
        """
        simulate = simulate if isinstance(simulate, bool) else False
        intent_level = intent_level if isinstance(intent_level, (str, int)) else self._default_intent_level
        col_sim = {"column": [], "order": [], "method": []}
        canonical = self._get_canonical(canonical)
        size = canonical.shape[0] if isinstance(canonical, pa.Table) else kwargs.pop('size', 1000)
        # test if there is any intent to run
        if not self._pm.has_intent(intent_level):
            raise ValueError(f"intent '{intent_level}' is not in [{self._pm.get_intent()}]")
        level_key = self._pm.join(self._pm.KEY.intent_key, intent_level)
        for order in sorted(self._pm.get(level_key, {})):
            for method, params in self._pm.get(self._pm.join(level_key, order), {}).items():
                try:
                    if method in self.__dir__():
                        if simulate:
                            col_sim['column'].append(intent_level)
                            col_sim['order'].append(order)
                            col_sim['method'].append(method)
                            continue
                        params.update(params.pop('kwargs', {}))
                        params.update({'save_intent': False})
                        if isinstance(seed, int):
                            params.update({'seed': seed})
                        _ = params.pop('intent_creator', 'Unknown')
                        canonical = eval(f"self.{method}(canonical=canonical, **params)", globals(), locals())
                except ValueError as ve:
                    raise ValueError(f"intent '{intent_level}', order '{order}', method '{method}' failed with: {ve}")
                except TypeError as te:
                    raise TypeError(f"intent '{intent_level}', order '{order}', method '{method}' failed with: {te}")
        if simulate:
            return pa.Table.from_pydict(col_sim)
        return canonical

    """
        PRIVATE METHODS SECTION
    """

    @staticmethod
    def _extract_mask(column: pa.Array, condition: list, mask_null: bool=None):
        """Creates a mask of the column based on the condition list of tuples. The condition tuple
        is made up of a triumvirate of a comparison value or text, an operator such as less or equals and
        logic of how the result links to the next tuple. mask_null replaces null with False, else null retained
        """
        mask_null = mask_null if isinstance(mask_null, bool) else False
        if isinstance(condition, tuple):
            condition = [condition]
        is_cat = False
        if pa.types.is_dictionary(column.type):
            column = column.dictionary_decode()
            is_cat = True
        cond_list = []
        for (comparison, operator, logic) in condition:
            try:
                if operator == 'greater':
                    c_bool = pc.greater(column, comparison)
                elif operator == 'less':
                    c_bool = pc.less(column, comparison)
                elif operator == 'greater_equal':
                    c_bool = pc.greater_equal(column, comparison)
                elif operator == 'less_equal':
                    c_bool = pc.less_equal(column, comparison)
                elif operator == 'extract_regex':
                    c_bool = pc.extract_regex(column, comparison)
                    c_bool = c_bool.is_valid()
                elif operator == 'equal':
                    c_bool = pc.equal(column, comparison)
                elif operator == 'not_equal':
                    c_bool = pc.not_qual(column, comparison)
                elif operator == 'is_in':
                    c_bool = pc.is_in(column, comparison)
                elif operator == 'is_null':
                    c_bool = pc.is_null(column)
                else:
                    raise NotImplementedError(f"Currently the operator '{operator} is not implemented.")
            except ArrowNotImplementedError:
                raise ValueError(f"The operator '{operator}' is not supported for data type '{column.type}'.")
            if logic not in ['and', 'or', 'xor', 'and_not', 'and_', 'or_']:
                logic = 'or_'
            if logic in ['and', 'or']:
                logic = logic + '_'
            if logic not in ['xor', 'and_not', 'and_', 'or_']:
                raise ValueError(f"The logic '{logic}' is not implemented")
            cond_list.append((c_bool, logic))
        final_cond = cond_list[0][0]
        for idx in range(len(cond_list) - 1):
            final_cond = eval(f"pc.{cond_list[idx][1]}(final_cond, cond_list[idx+1][0])", globals(), locals())
        return final_cond.fill_null(mask_null)

    def _get_canonical(self, data: [pa.Table, str]) -> pa.Table:
        """
        :param data: a dataframe or action event to generate a dataframe
        :return: a pa.Table
        """
        if not data:
            return None
        if isinstance(data, pa.Table):
            return data
        if isinstance(data, str):
            if not self._pm.has_connector(connector_name=data):
                raise ValueError(f"The data connector name '{data}' is not in the connectors catalog")
            handler = self._pm.get_connector_handler(data)
            canonical = handler.load_canonical()
            return canonical
        raise ValueError(f"The canonical format is not recognised, {type(data)} passed")

    def _intent_builder(self, method: str, params: dict, exclude: list = None) -> dict:
        """builds the intent_params. Pass the method name and local() parameters
            Example:
                self._intent_builder(inspect.currentframe().f_code.co_name, **locals())

        :param method: the name of the method (intent). can use 'inspect.currentframe().f_code.co_name'
        :param params: the parameters passed to the method. use `locals()` in the caller method
        :param exclude: (optional) convenience parameter identifying param keys to exclude.
        :return: dict of the intent
        """
        exclude = []
        if 'canonical' in params.keys() and not isinstance(params.get('canonical'), (str, dict, list)):
            exclude.append('canonical')
        if 'other' in params.keys() and not isinstance(params.get('other'), (str, dict, list)):
            exclude.append('other')
        return super()._intent_builder(method=method, params=params, exclude=exclude)

