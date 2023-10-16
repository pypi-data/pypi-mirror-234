import inspect
import pandas as pd
import pyarrow as pa
from ds_capability.components.discovery import DataDiscovery
from ds_capability.intent.common_intent import CommonsIntentModel
from ds_capability.intent.abstract_feature_build_intent import AbstractFeatureBuildIntentModel
from ds_capability.components.commons import Commons


class FeatureBuildIntent(AbstractFeatureBuildIntentModel, CommonsIntentModel):

    """Feature data is representative data that, depending on its application, holds statistical and
    distributive characteristics of its real world counterpart. This component provides a set of actions
    that focuses on building a synthetic data through knowledge and statistical analysis"""


    def build_difference(self, canonical: pa.Table, other: [str, pa.Table], on_key: [str, list], drop_zero_sum: bool=None,
                         summary_connector: bool=None, flagged_connector: str=None, detail_connector: str=None,
                         unmatched_connector: str=None, seed: int=None, save_intent: bool=None,
                         intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                         remove_duplicates: bool=None) -> pa.Table:
        """returns the difference between two canonicals, joined on a common and unique key.
        The ``on_key`` parameter can be a direct reference to the canonical column header or to an environment
        variable. If the environment variable is used ``on_key`` should be set to ``"${<<YOUR_ENVIRON>>}"`` where
        <<YOUR_ENVIRON>> is the environment variable name.

        If the ``flagged connector`` parameter is used, a report flagging mismatched left data with right data
        is produced for this connector where 1 indicate a difference and 0 they are the same. By default this method
        returns this report but if this parameter is set the original canonical returned. This allows a canonical
        pipeline to continue through the component while outputting the difference report.

        If the ``detail connector`` parameter is used, a detail report of the difference where the left and right
        values that differ are shown.

        If the ``unmatched connector`` parameter is used, the on_key's that don't match between left and right are
        reported

        :param canonical: a pa.Table as the reference table
        :param other: a direct pa.Table or reference to a connector.
        :param on_key: The name of the key that uniquely joins the canonical to others
        :param drop_zero_sum: (optional) drops rows and columns which has a total sum of zero differences
        :param summary_connector: (optional) a connector name where the summary report is sent
        :param flagged_connector: (optional) a connector name where the differences are flagged
        :param detail_connector: (optional) a connector name where the differences are shown
        :param unmatched_connector: (optional) a connector name where the unmatched keys are shown
        :param seed: (optional) this is a placeholder, here for compatibility across methods
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
        :return: a pa.Table
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intent action
        canonical = self._get_canonical(canonical)
        other = self._get_canonical(other)
        seed = seed if isinstance(seed, int) else self._seed()
        drop_zero_sum = drop_zero_sum if isinstance(drop_zero_sum, bool) else False
        flagged_connector = self._extract_value(flagged_connector)
        summary_connector = self._extract_value(summary_connector)
        detail_connector = self._extract_value(detail_connector)
        unmatched_connector = self._extract_value(unmatched_connector)
        on_key = Commons.list_formatter(self._extract_value(on_key))
        left_diff = Commons.list_diff(canonical.column_names, other.column_names, symmetric=False)
        right_diff = Commons.list_diff(other.column_names, canonical.column_names, symmetric=False)
        # drop columns
        tbl_canonical = canonical.drop_columns(left_diff)
        tbl_other = other.drop_columns(right_diff)
        # pandas
        df_canonical = tbl_canonical.to_pandas()
        df_other = tbl_other.to_pandas()
        # sort
        df_canonical.sort_values(on_key, inplace=True)
        df_other.sort_values(on_key, inplace=True)
        df_other = df_other.loc[:, df_canonical.columns.to_list()]

        # unmatched report
        if isinstance(unmatched_connector, str):
            if self._pm.has_connector(unmatched_connector):
                left_merge = pd.merge(df_canonical, df_other, on=on_key, how='left', suffixes=('', '_y'), indicator=True)
                left_merge = left_merge[left_merge['_merge'] == 'left_only']
                left_merge = left_merge[left_merge.columns[~left_merge.columns.str.endswith('_y')]]
                right_merge = pd.merge(df_canonical, df_other, on=on_key, how='right', suffixes=('_y', ''), indicator=True)
                right_merge = right_merge[right_merge['_merge'] == 'right_only']
                right_merge = right_merge[right_merge.columns[~right_merge.columns.str.endswith('_y')]]
                unmatched = pd.concat([left_merge, right_merge], axis=0, ignore_index=True)
                unmatched = unmatched.set_index(on_key, drop=True).reset_index(drop=True)
                unmatched.insert(0, 'found_in', unmatched.pop('_merge'))
                handler = self._pm.get_connector_handler(unmatched_connector)
                handler.persist_canonical(pa.Table.from_pandas(unmatched))
            else:
                raise ValueError(f"The connector name {unmatched_connector} has been given but no Connect Contract added")

        # remove non-matching rows
        df = pd.merge(df_canonical, df_other, on=on_key, how='inner', suffixes=('_x', '_y'))
        df_x = df.filter(regex='(_x$)', axis=1)
        df_y = df.filter(regex='(_y$)', axis=1)
        df_x.columns = df_x.columns.str.removesuffix('_x')
        df_y.columns = df_y.columns.str.removesuffix('_y')
        # flag the differences
        diff = df_x.ne(df_y).astype(int)
        if drop_zero_sum:
            diff = diff.loc[(diff != 0).any(axis=1),(diff != 0).any(axis=0)]
        # add back the keys
        for n in range(len(on_key)):
            diff.insert(n, on_key[n], df[on_key[n]].iloc[diff.index])

        # detailed report
        if isinstance(detail_connector, str):
            if self._pm.has_connector(detail_connector):
                diff_comp = df_x.astype(str).compare(df_y.astype(str)).fillna('-')
                for n in range(len(on_key)):
                    diff_comp.insert(n, on_key[n], df[on_key[n]].iloc[diff_comp.index])
                diff_comp.columns = ['_'.join(col) for col in diff_comp.columns.values]
                diff_comp.columns = diff_comp.columns.str.replace(r'_self$', '_x', regex=True)
                diff_comp.columns = diff_comp.columns.str.replace(r'_other$', '_y', regex=True)
                diff_comp.columns = diff_comp.columns.str.replace(r'_$', '', regex=True)
                diff_comp = diff_comp.sort_values(on_key)
                diff_comp = diff_comp.reset_index(drop=True)
                handler = self._pm.get_connector_handler(detail_connector)
                handler.persist_canonical(pa.Table.from_pandas(diff_comp))
            else:
                raise ValueError(f"The connector name {detail_connector} has been given but no Connect Contract added")

        # summary report
        if isinstance(summary_connector, str):
            if self._pm.has_connector(summary_connector):
                summary = diff.drop(on_key, axis=1).sum().reset_index()
                summary.columns = ['Attribute', 'Summary']
                summary = summary.sort_values(['Attribute'])
                indicator = pd.merge(df_canonical[on_key], df_other[on_key], on=on_key, how='outer', indicator=True)
                count = indicator['_merge'].value_counts().to_frame().reset_index().replace('both', 'matching')
                count.columns = ['Attribute', 'Summary']
                summary = pd.concat([count, summary], axis=0).reset_index(drop=True)
                handler = self._pm.get_connector_handler(summary_connector)
                handler.persist_canonical(pa.Table.from_pandas(summary))
            else:
                raise ValueError(f"The connector name {summary_connector} has been given but no Connect Contract added")

        # flagged report
        if isinstance(flagged_connector, str):
            if self._pm.has_connector(flagged_connector):
                diff = diff.sort_values(on_key)
                diff = diff.reset_index(drop=True)
                handler = self._pm.get_connector_handler(flagged_connector)
                handler.persist_canonical(pa.Table.from_pandas(diff))
                return canonical
            raise ValueError(f"The connector name {flagged_connector} has been given but no Connect Contract added")

        if drop_zero_sum:
            diff = diff.sort_values(on_key)
            diff = diff.reset_index(drop=True)

        return pa.Table.from_pandas(diff)

    def build_profiling(self, canonical: pa.Table, profiling: str, headers: [str, list]=None, d_types: [str, list]=None,
                        regex: [str, list]=None, drop: bool=None, connector_name: str=None, seed: int=None,
                        save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                        replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ Data profiling provides, analyzing, and creating useful summaries of data. The process yields a high-level
        overview which aids in the discovery of data quality issues, risks, and overall trends. It can be used to
        identify any errors, anomalies, or patterns that may exist within the data. There are three types of data
        profiling available 'dictionary', 'schema' or 'quality'

        :param canonical: a direct or generated pd.DataFrame. see context notes below
        :param profiling: The profiling name. Options are 'dictionary', 'schema' or 'quality'
        :param headers: (optional) a filter of headers from the 'other' dataset
        :param drop: (optional) to drop or not drop the headers if specified
        :param d_types: (optional) a filter on data type for the 'other' dataset. int, float, bool, object
        :param regex: (optional) a regular expression to search the headers. example '^((?!_amt).)*$)' excludes '_amt'
        :param connector_name::(optional) a connector name where the outcome is sent
        :param seed:(optional) this is a placeholder, here for compatibility across methods
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
        :return: a pa.Table
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intent action
        canonical = self._get_canonical(canonical)
        if d_types is None:
            d_types = []
        columns = Commons.filter_headers(canonical, headers=headers, d_types=d_types, regex=regex, drop=drop)
        _seed = self._seed() if seed is None else seed
        if profiling == 'dictionary':
            result =  DataDiscovery.data_dictionary(canonical=canonical, table_cast=True, stylise=False)
        elif profiling == 'quality':
            result =  DataDiscovery.data_quality(canonical=canonical, stylise=False)
        elif profiling == 'schema':
            result = DataDiscovery.data_schema(canonical=canonical, stylise=False)
        else:
            raise ValueError(f"The report name '{profiling}' is not recognised. Use 'dictionary', 'schema' or 'quality'")
        if isinstance(connector_name, str):
            if self._pm.has_connector(connector_name):
                handler = self._pm.get_connector_handler(connector_name)
                handler.persist_canonical(result)
                return canonical
            raise ValueError(f"The connector name {connector_name} has been given but no Connect Contract added")
        return result
