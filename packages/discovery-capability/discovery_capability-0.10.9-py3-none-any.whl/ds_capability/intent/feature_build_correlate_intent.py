import inspect
from typing import Any
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc

from ds_capability.components.commons import Commons
from ds_capability.components.discovery import DataDiscovery
from ds_capability.intent.feature_build_model_intent import FeatureBuildModelIntent


# noinspection PyArgumentList
class FeatureBuildCorrelateIntent(FeatureBuildModelIntent):

    def correlate_number(self, canonical: pa.Table, header: str, choice: [int, float, str]=None, choice_header: str=None,
                         to_header: str=None, precision: int=None, jitter: [int, float, str]=None, offset: [int, float, str]=None,
                         code_str: Any=None, lower: [int, float]=None, upper: [int, float]=None, keep_zero: bool=None,
                         seed: int=None, save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                         replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ correlate a list of continuous values adjusting those values, or a subset of those values, with a
        normalised jitter (std from the value) along with a value offset. ``choice``, ``jitter`` and ``offset``
        can accept environment variable string names starting with ``${`` and ending with ``}``.

        If the choice is an int, it represents the number of rows to choose. If the choice is a float it must be
        between 1 and 0 and represent a percentage of rows to choose.

        :param canonical: a pa.Table as the reference table
        :param header: the header in the Table to correlate
        :param choice: (optional) The number of values to choose to apply the change to. Can be an environment variable.
        :param choice_header: (optional) those not chosen are given the values of the given header
        :param to_header: (optional) an optional name to call the column
        :param precision: (optional) to what precision the return values should be
        :param offset: (optional) a fixed value to offset or if str an operation to perform using @ as the header value.
        :param code_str: (optional) passing a str lambda function. e.g. 'lambda x: (x - 3) / 2''
        :param jitter: (optional) a perturbation of the value where the jitter is a random normally distributed std
        :param precision: (optional) how many decimal places. default to 3
        :param seed: (optional) the random seed. defaults to current datetime
        :param keep_zero: (optional) if True then zeros passed remain zero despite a change, Default is False
        :param lower: a minimum value not to go below
        :param upper: a max value not to go above
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        if not isinstance(header, str) or header not in canonical.column_names:
            raise ValueError(f"The header '{header}' can't be found in the canonical headers")
        seed = seed if isinstance(seed, int) else self._seed()
        s_values = canonical.column(header).to_pandas()
        s_others = s_values.copy()
        other_size = s_others.size
        offset = self._extract_value(offset)
        keep_zero = keep_zero if isinstance(keep_zero, bool) else False
        precision = precision if isinstance(precision, int) else 3
        lower = lower if isinstance(lower, (int, float)) else float('-inf')
        upper = upper if isinstance(upper, (int, float)) else float('inf')
        # mark the zeros and nulls
        null_idx = s_values[s_values.isna()].index
        zero_idx = s_values.where(s_values == 0).dropna().index if keep_zero else []
        # choose the items to jitter
        if isinstance(choice, (str, int, float)):
            size = s_values.size
            choice = self._extract_value(choice)
            choice = int(choice * size) if isinstance(choice, float) and 0 <= choice <= 1 else int(choice)
            choice = choice if 0 <= choice < size else size
            gen = np.random.default_rng(seed=seed)
            choice_idx = gen.choice(s_values.index, size=choice, replace=False)
            choice_idx = [choice_idx] if isinstance(choice_idx, int) else choice_idx
            s_values = s_values.iloc[choice_idx]
        if isinstance(jitter, (str, int, float)) and s_values.size > 0:
            jitter = self._extract_value(jitter)
            size = s_values.size
            gen = np.random.default_rng(seed)
            results = gen.normal(loc=0, scale=jitter, size=size)
            s_values = s_values.add(results)
        # set code_str
        if isinstance(code_str, str) and s_values.size > 0:
            if code_str.startswith('lambda'):
                s_values = s_values.transform(eval(code_str))
            else:
                code_str = code_str.replace("@", 'x')
                s_values = s_values.transform(lambda x: eval(code_str))
        # set offset for all values
        if isinstance(offset, (int, float)) and offset != 0 and s_values.size > 0:
            s_values = s_values.add(offset)
        # set the changed values
        if other_size == s_values.size:
            s_others = s_values
        else:
            s_others.iloc[s_values.index] = s_values
        # max and min caps
        s_others = pd.Series([upper if x > upper else x for x in s_others])
        s_others = pd.Series([lower if x < lower else x for x in s_others])
        if isinstance(keep_zero, bool) and keep_zero:
            if other_size == zero_idx.size:
                s_others = 0 * zero_idx.size
            else:
                s_others.iloc[zero_idx] = 0
        if other_size == null_idx.size:
            s_others = np.nan * null_idx.size
        else:
            s_others.iloc[null_idx] = np.nan
        s_others = s_others.round(precision)
        if precision == 0 and not s_others.isnull().any():
            s_others = s_others.astype(int)
        rtn_list = s_others.to_list()
        rtn_arr = pa.NumericArray.from_pandas(rtn_list)
        if rtn_arr.type.equals('double'):
            try:
                rtn_arr = pa.array(rtn_arr, pa.int64())
            except pa.lib.ArrowInvalid:
                pass
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([rtn_arr], names=[to_header]))

    def correlate_discrete_intervals(self, canonical: pa.Table, header: str, granularity: [int, float, list]=None,
                                     lower: [int, float]=None, upper: [int, float]=None, categories: list=None,
                                     to_header: str=None, precision: int=None, seed: int=None, save_intent: bool=None,
                                     intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                                     remove_duplicates: bool=None) -> pa.Table:
        """ converts continuous representation into discrete representation through interval categorisation

        :param canonical: a pa.Table as the reference table
        :param header: the header in the Table to correlate
        :param granularity: (optional) the granularity of the analysis across the range. Default is 3
                int passed - represents the number of periods
                float passed - the length of each interval
                list[tuple] - specific interval periods e.g []
                list[float] - the percentile or quantities, All should fall between 0 and 1
        :param lower: (optional) the lower limit of the number value. Default min()
        :param upper: (optional) the upper limit of the number value. Default max()
        :param to_header: (optional) an optional name to call the column
        :param precision: (optional) The precision of the range and boundary values. by default set to 5.
        :param categories:(optional)  a set of labels the same length as the intervals to name the categories
        :param seed: (optional) the random seed. defaults to current datetime
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        if not isinstance(header, str) or header not in canonical.column_names:
            raise ValueError(f"The header '{header}' can't be found in the canonical headers")
        seed = seed if isinstance(seed, int) else self._seed()
        rtn_arr = DataDiscovery.to_discrete_intervals(array=canonical.column(header), granularity=granularity,
                                                      lower=lower, upper=upper, categories=categories,
                                                      precision=precision)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([rtn_arr.dictionary_encode()], names=[to_header]))

    def correlate_on_condition(self, canonical: pa.Table, header: str, other: str, condition: list,
                               value: [int, float, bool, str], fill_null: [int, float,str]=None,
                               default: [int, float, bool, str]=None, to_header: str=None, seed: int=None, save_intent: bool=None,
                               intent_order: int=None, intent_level: [int, str]=None, replace_intent: bool=None,
                               remove_duplicates: bool=None) -> pa.Table:
        """ correlates a named header to other header where the condition is met and replaces the header column
        value with a constant or value at the same index of an array. The condition is a list of triple tuples in
        the form: [(comparison, operation, logic)] where comparison is the thing to look for, the operation, what
        to do with it and the logic if you are chaining tuples, the logic to join them. An example might be:

                [(1, 'greater', 'or'), (-1, 'less', None)]
                [(pa.array(['INACTIVE', 'PENDING']), 'is_in', None)]

        The operator and logic are taken from pyarrow.compute and are:

                operator => 'extract_regex','equal','greater','less','greater_equal','less_equal','not_equal','is_in'
                logic => 'and','or','xor','and_not'

        :param canonical: a pa.Table as the reference table
        :param header: the header for the target values to change
        :param other: the other header to correlate
        :param condition: a tuple or tuples of
        :param value: a constant value. If the value is a string starting @ then a header values are taken
        :param default: (optional) a default constant if not value. A string starting @ then a default name is taken
        :param to_header: (optional) an optional name to call the column
        :param fill_null: (optional) if nulls in the other they require a value representation.
        :param seed: (optional) the random seed. defaults to current datetime
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        if not isinstance(header, str) or header not in canonical.column_names:
            raise ValueError(f"The header '{header}' can't be found in the canonical headers")
        seed = seed if isinstance(seed, int) else self._seed()
        h_col = canonical.column(header).combine_chunks()
        o_col = canonical.column(other).combine_chunks()
        if pa.types.is_dictionary(o_col.type):
            o_col = o_col.dictionary_decode()
        if fill_null is not None:
            o_col = o_col.fill_null(fill_null)
        cond_list = []
        for (comparison, op, logic) in condition:
            if op == 'greater':
                c_bool = pc.greater(o_col, comparison)
            elif op == 'less':
                c_bool = pc.less(o_col, comparison)
            elif op == 'greater_equal':
                c_bool = pc.greater_equal(o_col, comparison)
            elif op == 'less_equal':
                c_bool = pc.less_equal(o_col, comparison)
            elif op == 'extract_regex':
                c_bool = pc.extract_regex(o_col, comparison)
                c_bool = c_bool.is_valid()
            elif op == 'equal':
                c_bool = pc.equal(o_col, comparison)
            elif op == 'not_equal':
                c_bool = pc.not_qual(o_col, comparison)
            elif op == 'is_in':
                c_bool = pc.is_in(o_col, comparison)
            else:
                raise NotImplementedError(f"Currently the operation '{op} is not implemented")
            if logic not in ['and', 'or', 'xor', 'and_not', 'and_', 'or_']:
                logic = 'and_'
            if logic in ['and', 'or']:
                logic = logic + '_'
            if logic not in ['xor', 'and_not', 'and_', 'or_']:
                raise ValueError(f"The logic '{logic}' is not implemented")
            cond_list.append((c_bool, logic))
        final_cond = cond_list[0][0]
        for idx in range(len(cond_list) - 1):
            final_cond = eval(f"pc.{cond_list[idx][1]}(final_cond, cond_list[idx+1][0])", globals(), locals())
        # check the value
        if isinstance(value, str) and value.startswith('@'):
            value = canonical.column(value[1:]).combine_chunks()
        if isinstance(default, str) and default.startswith('@'):
            default = canonical.column(default[1:]).combine_chunks()
        elif default is None:
            default = h_col
            # replace and add it back to the original table
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pc.if_else(final_cond, value, default)], names=[to_header]))

    def correlate_column_join(self, canonical: pa.Table, header: str, others: [str, list], drop_others: bool=None,
                              sep: str=None, to_header: str=None, seed: int=None, save_intent: bool=None, intent_order: int=None,
                              intent_level: [int, str]=None, replace_intent: bool=None,
                              remove_duplicates: bool=None) -> pa.Table:
        """ creates a composite new column made up of other columns. The new column replaces the header column and the
        others are dropped unless the appropriate parameters are set.

        :param canonical: a pa.Table as the reference table
        :param header: the header for the target values to change
        :param others: the other headers to join
        :param drop_others: drop the others header columns. Default to true
        :param sep: a separator between each column value
        :param to_header: (optional) an optional name to call the column
        :param seed: (optional) the random seed. defaults to current datetime
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical ca
        :return: an equal length list of correlated values
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        seed = seed if isinstance(seed, int) else self._seed()
        drop_others = drop_others if isinstance(drop_others, bool) else True
        sep = sep if isinstance(sep, str) else ''
        others = Commons.list_formatter(others)
        if header in canonical.column_names:
            h_col = pc.cast(canonical.column(header).combine_chunks(), pa.string())
        else:
            h_col = header
        for n in others:
            if n in canonical.column_names:
                o_col = pc.cast(canonical.column(n).combine_chunks(), pa.string())
                if drop_others:
                    canonical = canonical.drop_columns(n)
            else:
                o_col = n
            h_col = pc.binary_join_element_wise(h_col, o_col, sep)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([h_col], names=[to_header]))

