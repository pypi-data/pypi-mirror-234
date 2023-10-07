from typing import Tuple

import pandas as pd
import numpy as np
import pyarrow as pa
import pyarrow.compute as pc
from ds_capability.components.commons import Commons


# noinspection PyArgumentList
class DataDiscovery(object):

    @staticmethod
    def interquartile_outliers(values: pa.Array, k_factor: float=None) -> Tuple[list, list]:
        """ The interquartile range (IQR), also called the midspread, middle 50%, or H‑spread, is a measure of
        statistical dispersion, being equal to the difference between 75th and 25th percentiles, or between upper
        and lower quartiles

        The IQR can be used to identify outliers by defining limits on the sample values that are a factor k of the
        IQR below the 25th percentile or above the 75th percentile. The common value for the factor k is the value 1.5.
        A factor k of 3 or more can be used to identify values that are extreme outliers.

        :param values: the values to be assessed
        :param k_factor: the k factor to apply beyond the 25th and 75th percentile, defaults to 1.5
        :return: a tuple of the lower and upper outliers as a list of index of the values
        """
        k_factor = k_factor if isinstance(k_factor, float) and 0 < k_factor <= 10 else 1.5
        values = values.drop_null()
        # calculate interquartile range
        q25, q75 = pc.quantile(values, [0.25, 0.75])
        iqr = pc.subtract(q75, q25).as_py()
        # calculate the outlier cutoff
        cut_off = pc.multiply(iqr, k_factor).as_py()
        lower, upper = pc.subtract(q25, cut_off).as_py(), pc.add(q75, cut_off).as_py()
        # identify outliers
        upper_outliers = values.filter(pc.greater_equal(values, upper)).to_pylist()
        lower_outliers = values.filter(pc.less_equal(values, lower)).to_pylist()
        return lower_outliers, upper_outliers

    @staticmethod
    def empirical_outliers(values: pa.Array, std_width: int=None) -> Tuple[list, list]:
        """ The empirical rule states that for a normal distribution, nearly all of the data will fall within three
        standard deviations of the mean.

        Given mu and sigma, a simple way to identify outliers is to compute a z-score for every value, which is
        defined as the number of standard deviations away value is from the mean. The 68–95–99.7 rule, also known as
        the empirical rule, is a shorthand used to remember the percentage of values that lie within a band around
        the mean in a normal distribution with a width of two, four and six standard deviations, respectively

        :param values: the values to be assessed
        :param std_width: (optional) A standard deviation away from the mean. Default is 3
        :return: a list of index of outliers
        """
        values = values.drop_null()
        std_width = std_width if isinstance(std_width, int) and 2 <= std_width <= 6 else 3
        data_mean, data_std = pc.mean(values).as_py(), pc.stddev(values).as_py()
        # identify outliers
        cut_off = pc.multiply(data_std, std_width).as_py()
        lower, upper = pc.subtract(data_mean, cut_off).as_py(), pc.add(data_mean, cut_off).as_py()
        # identify outliers
        upper_outliers = values.filter(pc.greater_equal(values, upper)).to_pylist()
        lower_outliers = values.filter(pc.less_equal(values, lower)).to_pylist()
        return lower_outliers, upper_outliers

    @staticmethod
    def data_quality(canonical: pa.Table, nulls_threshold: float=None, dom_threshold: float=None,
                     cat_threshold: int=None, capped_at: int=None, stylise: bool=None):
        """ Analyses a dataset, passed as a DataFrame and returns a quality summary

        :param canonical: The dataset, as a DataFrame.
        :param cat_threshold: The threshold for the max number of unique categories. Default is 60
        :param dom_threshold: The threshold limit of a dominant value. Default 0.98
        :param nulls_threshold: The threshold limit of a nulls value. Default 0.9
        :param capped_at: the row and column cap or 0 to ignore. default 5_000_000
        :param stylise: if the output is stylised for jupyter display
        :return: pd.DataFrame
        """
        # defaults
        cat_threshold = cat_threshold if isinstance(cat_threshold, int) else 60
        dom_threshold = dom_threshold if isinstance(dom_threshold, float) and 0 <= dom_threshold <= 1 else 0.98
        nulls_threshold = nulls_threshold if isinstance(nulls_threshold, float) and 0 <= nulls_threshold <= 1 else 0.95
        stylise = stylise if isinstance(stylise, bool) else False
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            row_count = int(round(cap / canonical.num_columns, 0))
            canonical = canonical.slice(0, row_count)
        # cast the values
        tbl = Commons.table_cast(canonical, cat_max=cat_threshold)
        # dictionary
        _null_columns = []
        _dom_columns = []
        _sparce_columns = []
        _date_columns = []
        _bool_columns = []
        _cat_columns = []
        _num_columns = []
        _int_columns = []
        _str_columns = []
        _nest_columns = []
        _other_columns = []
        _key_columns = []
        for n in tbl.column_names:
            c = tbl.column(n).combine_chunks()
            if pa.types.is_nested(c.type):
                _nest_columns.append(n)
                continue
            elif pa.types.is_string(c.type) and c.null_count != tbl.num_rows:
                _str_columns.append(n)
            elif pa.types.is_integer(c.type) and c.null_count != tbl.num_rows:
                _int_columns.append(n)
            elif pa.types.is_floating(c.type) and c.null_count != tbl.num_rows:
                _num_columns.append(n)
            elif pa.types.is_boolean(c.type) and c.null_count != tbl.num_rows:
                _bool_columns.append(n)
            elif pa.types.is_timestamp(c.type) or pa.types.is_time(c.type) and c.null_count != tbl.num_rows:
                _date_columns.append(n)
            elif pa.types.is_dictionary(c.type):
                _cat_columns.append(n)
                c = c.dictionary_decode()
            else:
                _other_columns.append(n)
                # nulls and
            if c.null_count/tbl.num_rows > nulls_threshold:
                _null_columns.append(n)
            elif c.null_count / tbl.num_rows > 0.66:
                _sparce_columns.append(n)
            elif pc.count_distinct(c.drop_null()).as_py() == pc.count(c).as_py():
                _key_columns.append(n)
            elif 1-(pc.count_distinct(c.drop_null()).as_py()/pc.count(c).as_py()) > dom_threshold:
                _dom_columns.append(n)
        # dictionary
        _usable_columns = _date_columns + _bool_columns + _cat_columns + _num_columns + _int_columns + _str_columns
        _null_avg = len(_null_columns) / canonical.num_columns
        _dom_avg = len(_dom_columns) / canonical.num_columns
        _quality_avg = int(round(100 - (((_null_avg + _dom_avg) / 2) * 100), 0))
        _usable = int(round((len(_usable_columns) / canonical.num_columns) * 100, 2))
        # duplicate
        _dup_columns = []
        for i in range(0, len(tbl.column_names)):
            col_1 = tbl.column_names[i]
            for col_2 in tbl.column_names[i + 1:]:
                if tbl.column(col_1).equals(tbl.column(col_2)):
                    _dup_columns.append(col_2)
        # time
        _dt_today = pd.to_datetime('today')
        mem_usage = canonical.get_total_buffer_size()
        _tbl_mem = f"{mem_usage >> 20} Mb" if mem_usage >> 20 > 0 else f"{mem_usage} bytes"
        mem_usage = pa.total_allocated_bytes()
        _tot_mem = f"{mem_usage >> 20} Mb" if mem_usage >> 20 > 0 else f"{mem_usage} bytes"
        report = {
            'timestamp': {'readable': _dt_today.strftime('%d %B %Y %I:%M %p'),
                          'semantic': _dt_today.strftime('%Y-%m-%d %H:%M:%S')},
            'score': {'quality_avg': f"{_quality_avg}%", 'usability_avg': f"{_usable}%"},
            'data_shape': {'tbl_memory': _tbl_mem, 'total_allocated': _tot_mem,
                           'rows': canonical.num_rows, 'columns': canonical.num_columns},
            'data_type': {'floating': len(_num_columns), 'integer': len(_int_columns),
                          'category': len(_cat_columns), 'datetime': len(_date_columns),
                          'bool': len(_bool_columns),'string': len(_str_columns),
                          'nested': len(_nest_columns), 'others': len(_other_columns)},
            'usability': {'mostly_null': len(_null_columns),
                          'predominance': len(_dom_columns),
                          'sparse': len(_sparce_columns),
                          'duplicate': len(_dup_columns),
                          'candidate_keys': len(_key_columns)}
        }
        # convert to multi-index DataFrame
        result = pd.DataFrame.from_dict(report, orient="index").stack().to_frame()
        result = pd.DataFrame(result[0].values.tolist(), index=result.index, columns=['summary'])
        result['summary'] = result['summary'].apply(str).str.replace('.0', '', regex=False)
        result = result.reset_index(names=['sections', 'elements'])
        if stylise:
            return Commons.report(result, index_header='sections', bold=['elements'])
        reference = [_num_columns, _int_columns, _cat_columns, _date_columns, _bool_columns, _str_columns, _nest_columns,
                 _other_columns, _null_columns, _dom_columns, _sparce_columns, _dup_columns, _key_columns]
        return Commons.table_append(pa.Table.from_pandas(result),
                                    pa.table([pa.array([[]] * 8 + reference, pa.list_(pa.string()))], names=['columns']))


    @staticmethod
    def data_dictionary(canonical: pa.Table, table_cast: bool=None, display_width: int=None, stylise: bool=None,
                        capped_at: int=None):
        """ The data dictionary for a given canonical

        :param canonical: The canonical to interpret
        :param table_cast: attempt to cast columns to the content
        :param display_width: the width of the display
        :param stylise: if the output is stylised for jupyter display
        :param capped_at: the row and column cap or 0 to ignore. default 5_000_000
        :return: a pa.Table or stylised pandas
        """
        display_width = display_width if isinstance(display_width, int) else 50
        stylise = stylise if isinstance(stylise, bool) else False
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            row_count = int(round(cap / canonical.num_columns, 0))
            canonical = canonical.slice(0, row_count)
        record = []
        labels = [f'Attributes', 'DataType', 'Nulls', 'Dominate', 'Valid', 'Unique', 'Observations']
        # attempt cast
        if isinstance(table_cast, bool) and table_cast:
            canonical = Commons.table_cast(canonical)
        for c in canonical.column_names:
            column = canonical.column(c).combine_chunks()
            if pa.types.is_nested(column.type):
                s = str(column.slice(0,20).to_pylist())
                if len(s) > display_width:
                    s = s[:display_width] + "..."
                record.append([c,'nested',0,0,1,1,s])
                continue
            # data type
            line = [c,
                    'category' if pc.starts_with(str(column.type), 'dict').as_py() else str(column.type),
                    # null percentage
                    round(column.null_count / canonical.num_rows, 3)]
            # dominant percentage
            arr_vc = column.value_counts()
            value = arr_vc.filter(pc.equal(arr_vc.field(1), pc.max(arr_vc.field(1)))).field(1)[0].as_py()
            line.append(round(value / canonical.num_rows, 3))
            # valid
            line.append(pc.sum(column.is_valid()).as_py())
            # unique
            line.append(pc.count(column.unique()).as_py())
            # observations
            vc = column.drop_null().value_counts()
            if pa.types.is_dictionary(column.type):
                t = pa.table([vc.field(1), vc.field(0).dictionary], names=['v', 'n']).sort_by([("v", "descending")])
            else:
                t = pa.table([vc.field(1), vc.field(0)], names=['v', 'n']).sort_by([("v", "descending")])
            s = str(t.column('n').to_pylist())
            if len(s) > display_width:
                s = s[:display_width] + "..."
            line.append(s)
            record.append(line)
        df = pd.DataFrame(record, columns=labels)
        if stylise:
            style = [{'selector': 'th', 'props': [('font-size', "120%"), ("text-align", "center")]},
                     {'selector': '.row_heading, .blank', 'props': [('display', 'none;')]}]
            df_style = df.style.set_table_styles(style)
            _ = df_style.applymap(DataDiscovery._highlight_null_dom, subset=['Nulls', 'Dominate'])
            _ = df_style.applymap(lambda x: 'color: white' if x > 0.98 else 'color: black', subset=['Nulls', 'Dominate'])
            _ = df_style.applymap(DataDiscovery._dtype_color, subset=['DataType'])
            _ = df_style.applymap(DataDiscovery._color_unique, subset=['Unique'])
            _ = df_style.applymap(lambda x: 'color: white' if x < 2 else 'color: black', subset=['Unique'])
            _ = df_style.format({'Nulls': "{:.1%}", 'Dominate': '{:.1%}'})
            _ = df_style.set_caption(f"dataset has {canonical.num_columns} columns")
            _ = df_style.set_properties(subset=['Attributes'],  **{'font-weight': 'bold', 'font-size': "120%"})
            return df_style
        return pa.Table.from_pandas(df)

    @staticmethod
    def data_schema(canonical: pa.Table, table_cast: bool=None, capped_at: int=None, stylise: bool=None):
        """ The data dictionary for a given canonical

        :param canonical: The canonical to interpret
        :param table_cast: (optional) attempt to cast columns to the content
        :param capped_at: the row and column cap or 0 to ignore. default 5_000_000
        :param stylise: (optional) if the output is stylised for jupyter display
        :return: a pa.Table or stylised pandas
        """
        stylise = stylise if isinstance(stylise, bool) else False
        cap = capped_at if isinstance(capped_at, int) else 5_000_000
        if canonical.num_rows*canonical.num_columns > cap > 0:
            row_count = int(round(cap / canonical.num_columns, 0))
            canonical = canonical.slice(0, row_count)
        if isinstance(table_cast, bool) and table_cast:
            canonical = Commons.table_cast(canonical)
        record = []
        for n in canonical.column_names:
            c = canonical.column(n).combine_chunks()
            if pa.types.is_nested(c.type) or pa.types.is_binary(c.type) or pc.equal(c.null_count, canonical.num_rows).as_py():
                continue
            if pa.types.is_dictionary(c.type):
                vc = c.drop_null().value_counts()
                t = pa.table([vc.field(1), vc.field(0).dictionary], names=['v','n']).sort_by([("v", "descending")])
                record.append([n, 'categories', t.column('n').to_pylist()])
                _ = pc.round(pc.divide_checked(t.column('v').cast(pa.float64()), pc.sum(t.column('v'))),3).to_pylist()
                record.append([n, 'frequency', _])
                record.append([n, 'type', 'category'])
                record.append([n, 'measure', 'discrete'])
                record.append([n, 'nulls', c.null_count])
                record.append([n, 'valid', pc.sum(c.is_valid()).as_py()])
            elif pa.types.is_integer(c.type) or pa.types.is_floating(c.type):
                precision = Commons.column_precision(c)
                intervals = DataDiscovery.to_discrete_intervals(column=c, granularity=5, categories=['A','B','C','D','E'])
                vc = intervals.dictionary_encode().drop_null().value_counts()
                t = pa.table([vc.field(1), vc.field(0).dictionary], names=['v','n']).sort_by([("n", "ascending")])
                record.append([n, 'intervals', "['lower','low','mid','high','higher']"])
                _ = pc.round(pc.divide_checked(t.column('v').cast(pa.float64()), pc.sum(t.column('v'))),3).to_pylist()
                record.append([n, 'frequency', _])
                record.append([n, 'type', c.type])
                record.append([n, 'measure', 'temporal' if pa.types.is_temporal(c.type) else 'continuous'])
                record.append([n, 'nulls', c.null_count])
                record.append([n, 'valid', pc.sum(c.is_valid()).as_py()])
                record.append([n, 'mean', pc.round(pc.mean(c),precision).as_py()])
                record.append([n, 'std', pc.round(pc.sqrt(pc.variance(c)),precision).as_py()])
                record.append([n, 'max', pc.round(pc.max(c),precision).as_py()])
                record.append([n, '75%', pc.round(pc.quantile(c,0.75),precision).to_pylist()[0]])
                record.append([n, '50%', pc.round(pc.quantile(c,0.5),precision).to_pylist()[0]])
                record.append([n, '25%', pc.round(pc.quantile(c,0.25),precision).to_pylist()[0]])
                record.append([n, 'min', pc.round(pc.min(c),precision).as_py()])
                # skew
                values = c.slice(0, 100000).to_pandas()
                record.append([n, 'skew', round(values.skew(), 3)])
                s_bins = [-np.inf, -1, -0.5, -0.1, 0.1, 0.5, 1, np.inf]
                s_names = ['highly left', 'medium left', 'light left', 'normal', 'light right', 'medium right',
                           'highly right']
                _skew_bin = list(pd.cut([values.skew()], s_bins, labels=s_names))[0]
                record.append([n, 'skew bias', _skew_bin])
                # kurtosis
                record.append([n, 'kurtosis', round(values.kurtosis(), 3)])
                k_bins = [-np.inf, 2.9, 3.1, np.inf]
                k_names = ['platykurtic', 'mesokurtic', 'leptokurtic']
                _kurt_bin = list(pd.cut([values.kurtosis()], k_bins, labels=k_names))[0]
                record.append([n, 'kurtosis_tail', _kurt_bin])
            elif pa.types.is_boolean(c.type):
                vc = c.drop_null().value_counts()
                t = pa.table([vc.field(1), vc.field(0)], names=['v', 'n']).sort_by([("n", "ascending")])
                record.append([n, 'boolean', t.column('n').to_pylist()])
                _ = pc.round(pc.divide_checked(t.column('v').cast(pa.float64()), pc.sum(t.column('v'))),3).to_pylist()
                record.append([n, 'frequency', _])
                record.append([n, 'type', c.type])
                record.append([n, 'measure', 'binary'])
                record.append([n, 'nulls', c.null_count])
                record.append([n, 'valid', pc.sum(c.is_valid()).as_py()])
            elif pa.types.is_timestamp(c.type) or pa.types.is_time(c.type):
                _ = pa.array(Commons.date2value(c.to_pylist()))
                intervals = DataDiscovery.to_discrete_intervals(column=_, granularity=5, categories=['A','B','C','D','E'])
                vc = intervals.dictionary_encode().drop_null().value_counts()
                t = pa.table([vc.field(1), vc.field(0).dictionary], names=['v','n']).sort_by([("n", "ascending")])
                record.append([n, 'intervals', "['older','old','mid','new','newer']"])
                _ = pc.round(pc.divide_checked(t.column('v').cast(pa.float64()), pc.sum(t.column('v'))),3).to_pylist()
                record.append([n, 'frequency', _])
                record.append([n, 'type', c.type])
                record.append([n, 'measure', 'temporal' if pa.types.is_temporal(c.type) else 'continuous'])
                record.append([n, 'nulls', c.null_count])
                record.append([n, 'valid', pc.sum(c.is_valid()).as_py()])
                record.append([n, 'oldest', pc.min(c).as_py()])
                record.append([n, 'newest', pc.max(c).as_py()])
            elif pa.types.is_string(c.type):
                record.append([n, 'type', c.type])
                record.append([n, 'nulls', c.null_count])
                record.append([n, 'sample', pc.sum(c.is_valid()).as_py()])
        df = pd.DataFrame(record, columns=['attributes', 'elements', 'values'])
        df['values'] = df['values'].astype(str)
        if stylise:
            return Commons.report(df, index_header='attributes', bold=['elements'])
        return pa.Table.from_pandas(df)

    @staticmethod
    def to_discrete_intervals(column: pa.Array, granularity: [int, float, list]=None, lower: [int, float]=None,
                              upper: [int, float]=None, categories: list=None, precision: int=None) -> pa.Array:
        """ creates discrete intervals from continuous values """
        # intend code block on the canonical
        granularity = granularity if isinstance(granularity, (int, float, list)) or granularity == 0 else 5
        granularity = len(categories) if isinstance(categories, list) else granularity
        precision = precision if isinstance(precision, int) else 5
        # firstly get the granularity
        lower = lower if isinstance(lower, (int, float)) else pc.min(column).as_py()
        upper = upper if isinstance(upper, (int, float)) else pc.max(column).as_py()
        s_values = column.to_pandas()
        if lower >= upper:
            upper = lower
            granularity = [(lower, upper, 'both')]
        if isinstance(granularity, (int, float)):
            # if granularity float then convert frequency to intervals
            if isinstance(granularity, float):
                # make sure frequency goes beyond the upper
                _end = upper + granularity - (upper % granularity)
                periods = pd.interval_range(start=lower, end=_end, freq=granularity).drop_duplicates()
                periods = periods.to_tuples().to_list()
                granularity = []
                while len(periods) > 0:
                    period = periods.pop(0)
                    if len(periods) == 0:
                        granularity += [(period[0], period[1], 'both')]
                    else:
                        granularity += [(period[0], period[1], 'left')]
            # if granularity int then convert periods to intervals
            else:
                periods = pd.interval_range(start=lower, end=upper, periods=granularity).drop_duplicates()
                granularity = periods.to_tuples().to_list()
        if isinstance(granularity, list):
            if all(isinstance(value, tuple) for value in granularity):
                if len(granularity[0]) == 2:
                    granularity[0] = (granularity[0][0], granularity[0][1], 'both')
                granularity = [(t[0], t[1], 'right') if len(t) == 2 else t for t in granularity]
            elif all(isinstance(value, float) and 0 < value < 1 for value in granularity):
                quantiles = list(set(granularity + [0, 1.0]))
                boundaries = s_values.quantile(quantiles).values
                boundaries.sort()
                granularity = [(boundaries[0], boundaries[1], 'both')]
                granularity += [(boundaries[i - 1], boundaries[i], 'right') for i in range(2, boundaries.size)]
            else:
                granularity = (lower, upper, 'both')
        granularity = [(np.round(p[0], precision), np.round(p[1], precision), p[2]) for p in granularity]
        # now create the categories
        conditions = []
        for interval in granularity:
            lower, upper, closed = interval
            if str.lower(closed) == 'neither':
                conditions.append((s_values > lower) & (s_values < upper))
            elif str.lower(closed) == 'right':
                conditions.append((s_values > lower) & (s_values <= upper))
            elif str.lower(closed) == 'both':
                conditions.append((s_values >= lower) & (s_values <= upper))
            else:
                conditions.append((s_values >= lower) & (s_values < upper))
        if isinstance(categories, list) and len(categories) == len(conditions):
            choices = categories
        else:
            if s_values.dtype.name.startswith('int'):
                choices = [f"{int(i[0])}->{int(i[1])}" for i in granularity]
            else:
                choices = [f"{i[0]}->{i[1]}" for i in granularity]
        # noinspection PyTypeChecker
        rtn_list = np.select(conditions, choices, default=None).tolist()
        return pa.StringArray.from_pandas(rtn_list)


    @staticmethod
    def _dtype_color(dtype: str):
        """Apply color to types"""
        if str(dtype).startswith('cat'):
            color = '#208a0f'
        elif str(dtype).startswith('int'):
            color = '#0f398a'
        elif str(dtype).startswith('float'):
            color = '#2f0f8a'
        elif str(dtype).startswith('date'):
            color = '#790f8a'
        elif str(dtype).startswith('bool'):
            color = '#08488e'
        elif str(dtype).startswith('str'):
            color = '#761d38'
        else:
            return ''
        return 'color: %s' % color

    @staticmethod
    def _highlight_null_dom(x: str):
        x = float(x)
        if not isinstance(x, float) or x < 0.65:
            return ''
        elif x < 0.85:
            color = '#ffede5'
        elif x < 0.90:
            color = '#fdcdb9'
        elif x < 0.95:
            color = '#fcb499'
        elif x < 0.98:
            color = '#fc9576'
        elif x < 0.99:
            color = '#fb7858'
        elif x < 0.997:
            color = '#f7593f'
        else:
            color = '#ec382b'
        return 'background-color: %s' % color

    @staticmethod
    def _color_unique(x: str):
        x = int(x)
        if not isinstance(x, int):
            return ''
        elif x < 2:
            color = '#ec382b'
        elif x < 3:
            color = '#a1cbe2'
        elif x < 5:
            color = '#84cc83'
        elif x < 10:
            color = '#a4da9e'
        elif x < 20:
            color = '#c1e6ba'
        elif x < 50:
            color = '#e5f5e0'
        elif x < 100:
            color = '#f0f9ed'
        else:
            return ''
        return 'background-color: %s' % color
