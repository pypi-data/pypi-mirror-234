import inspect
from typing import Any
import string
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from sklearn.impute import KNNImputer
from ds_capability.components.discovery import DataDiscovery
from scipy import stats
from ds_capability.intent.common_intent import CommonsIntentModel
from ds_capability.intent.abstract_feature_engineer_intent import AbstractFeatureEngineerIntentModel
from ds_capability.components.commons import Commons
from ds_capability.sample.sample_data import Sample, MappedSample


# noinspection PyArgumentList
class FeatureEngineerIntent(AbstractFeatureEngineerIntentModel, CommonsIntentModel):

    """Feature data is representative data that, depending on its application, holds statistical and
    distributive characteristics of its real world counterpart. This component provides a set of actions
    that focuses on building a synthetic data through knowledge and statistical analysis"""

    @property
    def sample_list(self) -> list:
        """A list of sample options"""
        return Sample().__dir__()

    @property
    def sample_map(self) -> list:
        """A list of sample options"""
        return MappedSample().__dir__()

    @staticmethod
    def sample_inspect(method: str):
        """"""
        if method in MappedSample().__dir__():
            i = inspect.signature(eval(f"MappedSample().{method}")).parameters
            rtn_lst = []
            for key, value in i.items():
                if key in ['size', 'shuffle', 'seed']:
                    continue
                rtn_lst.append(str(value)[:-7])
            return rtn_lst
        raise ValueError(f"The sample map name '{method}' was not found in the MappedSample class")

    def get_number(self, start: [int, float, str]=None, stop: [int, float, str]=None, canonical: pa.Table=None,
                   relative_freq: list=None, precision: int=None, ordered: str=None, at_most: int=None, size: int=None,
                   quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None, intent_order: int=None,
                   intent_level: [int, str]=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ returns a number in the range from_value to to_value. if only to_value given from_value is zero

        :param start: optional (signed) integer or float to start from. See below for str
        :param stop: (signed) integer or float the number sequence goes to but not include. See below
        :param canonical: (optional) a pa.Table to append the result table to
        :param relative_freq: (optional) a weighting pattern or probability that does not have to add to 1
        :param precision: (optional) the precision of the returned number. if None then assumes int value else float
        :param ordered: (optional) order the data ascending 'asc' or descending 'dec', values accepted 'asc' or 'des'
        :param at_most:  (optional)the most times a selection should be chosen
        :param to_header: (optional) an optional name to call the column
        :param size: (optional) the size of the sample
        :param quantity: (optional) a number between 0 and 1 representing data that isn't null
        :param seed: (optional) a seed value for the random function: default to None
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
        :return: a random number

        The values can be represented by an environment variable with the format '${NAME}' where NAME is the
        environment variable name
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        start = self._extract_value(start)
        stop = self._extract_value(stop)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if not isinstance(start, (int, float)) and not isinstance(stop, (int, float)):
            raise ValueError(f"either a 'from_value' or a 'from_value' and 'to_value' must be provided")
        if not isinstance(start, (float, int)):
            start = 0
        if not isinstance(stop, (float, int)):
            (start, stop) = (0, start)
        if stop <= start:
            raise ValueError("The number range must be a positive difference, where to_value <= from_value")
        at_most = 0 if not isinstance(at_most, int) else at_most
        #        size = size if isinstance(size, int) else 1
        seed = self._seed() if seed is None else seed
        precision = 3 if not isinstance(precision, int) else precision
        if precision == 0:
            start = int(round(start, 0))
            stop = int(round(stop, 0))
        is_int = True if (isinstance(stop, int) and isinstance(start, int)) else False
        if is_int:
            precision = 0
        # build the distribution sizes
        if isinstance(relative_freq, list) and len(relative_freq) > 1 and sum(relative_freq) > 1:
            freq_dist_size = self._freq_dist_size(relative_freq=relative_freq, size=size, seed=seed)
        else:
            freq_dist_size = [size]
        # generate the numbers
        rtn_list = []
        generator = np.random.default_rng(seed=seed)
        d_type = int if is_int else float
        bins = np.linspace(start, stop, len(freq_dist_size) + 1, dtype=d_type)
        for idx in np.arange(1, len(bins)):
            low = bins[idx - 1]
            high = bins[idx]
            if low >= high:
                continue
            elif at_most > 0:
                sample = []
                for _ in np.arange(at_most, dtype=d_type):
                    count_size = freq_dist_size[idx - 1] * generator.integers(2, 4, size=1)[0]
                    sample += list(set(np.linspace(bins[idx - 1], bins[idx], num=count_size, dtype=d_type,
                                                   endpoint=False)))
                if len(sample) < freq_dist_size[idx - 1]:
                    raise ValueError(f"The value range has insufficient samples to choose from when using at_most."
                                     f"Try increasing the range of values to sample.")
                rtn_list += list(generator.choice(sample, size=freq_dist_size[idx - 1], replace=False))
            else:
                if d_type == int:
                    rtn_list += generator.integers(low=low, high=high, size=freq_dist_size[idx - 1]).tolist()
                else:
                    choice = generator.random(size=freq_dist_size[idx - 1], dtype=float)
                    choice = np.round(choice * (high - low) + low, precision).tolist()
                    # make sure the precision
                    choice = [high - 10 ** (-precision) if x >= high else x for x in choice]
                    rtn_list += choice
        # order or shuffle the return list
        if isinstance(ordered, str) and ordered.lower() in ['asc', 'des']:
            rtn_list.sort(reverse=True if ordered.lower() == 'asc' else False)
        else:
            generator.shuffle(rtn_list)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        rtn_arr = pa.NumericArray.from_pandas(rtn_list)
        if rtn_arr.type.equals('double'):
            try:
                rtn_arr = pa.array(rtn_arr, pa.int64())
            except pa.lib.ArrowInvalid:
                pass
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([rtn_arr], names=[to_header]))

    def get_category(self, selection: list, size: int, canonical: pa.Table=None, relative_freq: list=None, encode: bool=None,
                     quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                     intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ returns a categorical as a string.

        :param selection: a list of items to select from
        :param size: size of the return
        :param canonical: (optional) a pa.Table to append the result table to
        :param relative_freq: a weighting pattern that does not have to add to 1
        :param encode: if the categorical should be returned encoded as a dictionary type or string type (default)
        :param quantity: a number between 0 and 1 representing the percentage quantity of the data
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: an item or list of items chosen from the list
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if len(selection) < 1:
            return [None] * size
        encode = encode if isinstance(encode, bool) else False
        seed = self._seed() if seed is None else seed
        relative_freq = relative_freq if isinstance(relative_freq, list) else [1]*len(selection)
        select_index = self._freq_dist_size(relative_freq=relative_freq, size=size, dist_length=len(selection),
                                                  dist_on='right', seed=seed)
        rtn_list = []
        for idx in range(len(select_index)):
            rtn_list += [selection[idx]]*select_index[idx]
        gen = np.random.default_rng(seed)
        gen.shuffle(rtn_list)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        if encode:
            return Commons.table_append(canonical, pa.table([pa.DictionaryArray.from_pandas(rtn_list).dictionary_encode()], names=[to_header]))
        return Commons.table_append(canonical, pa.table([pa.DictionaryArray.from_pandas(rtn_list)], names=[to_header]))

    def get_boolean(self, size: int, canonical: pa.Table=None, probability: float=None, quantity: float=None,
                    to_header: str=None,  seed: int=None, save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                    replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """A boolean discrete random distribution

        :param size: the size of the sample
        :param canonical: (optional) a pa.Table to append the result table to
        :param probability: a float between 0 and 1 of the probability of success. Default = 0.5
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        prob = probability if isinstance(probability, int) and 0 < probability < 1 else 0.5
        seed = self._seed(seed=seed)
        rtn_list = list(stats.bernoulli.rvs(p=probability, size=size, random_state=seed))
        rtn_list = list(map(bool, rtn_list))
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_datetime(self, start: Any, until: Any, canonical: pa.Table=None, relative_freq: list=None,
                     at_most: int=None, ordered: str=None, date_format: str=None, timezone: str=None,
                     time_unit: str=None, as_num: bool=None, ignore_time: bool=None, ignore_seconds: bool=None,
                     size: int=None, quantity: float=None, to_header: str=None,  seed: int=None, day_first: bool=None,
                     year_first: bool=None, save_intent: bool=None, intent_level: [int, str]=None,
                     intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ returns a random date between two date and/or times. weighted patterns can be applied to the overall date
        range. if a signed 'int' type is passed to the start and/or until dates, the inferred date will be the current
        date time with the integer being the offset from the current date time in 'days'.

        Note: If no patterns are set this will return a linearly random number between the range boundaries.

        :param timezone: (optional)
        :param time_unit: (optional) the time units for the timezone. Options 's' 'ms' 'us' or 'ns'
        :param start: the start boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp or int
        :param until: up until boundary of the date range can be str, datetime, pd.datetime, pd.Timestamp or int
        :param canonical: (optional) a pa.Table to append the result table to
        :param quantity: (optional) the quantity of values that are not null. Number between 0 and 1
        :param relative_freq: (optional) A pattern across the whole date range.
        :param at_most: (optional) the most times a selection should be chosen
        :param ordered: (optional) order the data ascending 'asc' or descending 'dec', values accepted 'asc' or 'des'
        :param ignore_time: ignore time elements and only select from Year, Month, Day elements. Default is False
        :param ignore_seconds: ignore second elements and only select from Year to minute elements. Default is False
        :param date_format: the string format of the date to be returned. if not set then pd.Timestamp returned
        :param as_num: returns a list of Matplotlib date values as a float. Default is False
        :param size: the size of the sample to return. Default to 1
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
        :param year_first: specifies if to parse with the year first
                    - If True parses dates with the year first, e.g. 10/11/12 is parsed as 2010-11-12.
                    - If both dayfirst and yearfirst are True, yearfirst is preceded (same as dateutil).

        :param day_first: specifies if to parse with the day first
                    - If True, parses dates with the day first, eg %d-%m-%Y.
                    - If False default to a preferred preference, normally %m-%d-%Y (but not strict)

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
        :return: a date or size of dates in the format given.
         """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if start is None or until is None:
            raise ValueError("The start or until parameters cannot be of NoneType")
        # Code block for intent
        time_unit = time_unit if isinstance(time_unit, str) and time_unit in ['s', 'ms', 'us', 'ns'] else 'us'
        as_num = as_num if isinstance(as_num, bool) else False
        ignore_seconds = ignore_seconds if isinstance(ignore_seconds, bool) else False
        ignore_time = ignore_time if isinstance(ignore_time, bool) else False
        seed = self._seed() if seed is None else seed
        # start = start.to_pydatetime() if isinstance(start, pd.Timestamp) else start
        # until = until.to_pydatetime() if isinstance(until, pd.Timestamp) else until
        if isinstance(start, int):
            start = (pd.Timestamp.now() + pd.Timedelta(days=start))
        start = pd.to_datetime(start, errors='coerce', dayfirst=day_first,
                               yearfirst=year_first)
        if isinstance(until, int):
            until = (pd.Timestamp.now() + pd.Timedelta(days=until))
        elif isinstance(until, dict):
            until = (start + pd.Timedelta(**until))
        until = pd.to_datetime(until, errors='coerce', dayfirst=day_first,
                               yearfirst=year_first)
        if start == until:
            rtn_list = pd.Series([start] * size)
        else:
            dt_tz = pd.Series(start).dt.tz
            _dt_start = Commons.date2value(start, day_first=day_first, year_first=year_first)[0]
            _dt_until = Commons.date2value(until, day_first=day_first, year_first=year_first)[0]
            precision = 15
            rtn_tbl = self.get_number(start=_dt_start, stop=_dt_until, relative_freq=relative_freq, at_most=at_most,
                                       ordered=ordered, precision=precision, size=size, seed=seed, save_intent=False)
            rtn_list = rtn_tbl.columns.pop(0).to_pylist()
            rtn_list = pd.Series(Commons.value2date(rtn_list, dt_tz=dt_tz))
        if ignore_time:
            rtn_list = pd.Series(pd.DatetimeIndex(rtn_list).normalize())
        if ignore_seconds:
            rtn_list = rtn_list.apply(lambda t: t.replace(second=0, microsecond=0, nanosecond=0))
        if as_num:
            return Commons.date2value(rtn_list)
        if isinstance(date_format, str) and len(rtn_list) > 0:
            rtn_list = rtn_list.dt.strftime(date_format)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        arr = pc.cast(pa.TimestampArray.from_pandas(rtn_list), pa.timestamp(time_unit, timezone))
        return Commons.table_append(canonical, pa.table([arr], names=[to_header]))

    def get_intervals(self, intervals: list, canonical: pa.Table=None, relative_freq: list=None, precision: int=None,
                      size: int=None, quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None,
                      intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                      remove_duplicates: bool=None) -> pa.Table:
        """ returns a number based on a list selection of tuple(lower, upper) interval

        :param intervals: a list of unique tuple pairs representing the interval lower and upper boundaries
        :param canonical: (optional) a pa.Table to append the result table to
        :param relative_freq: a weighting pattern or probability that does not have to add to 1
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        precision = precision if isinstance(precision, (float, int)) else 3
        seed = self._seed() if seed is None else seed
        if not all(isinstance(value, tuple) for value in intervals):
            raise ValueError("The intervals list must be a list of tuples")
        interval_tbl = self.get_category(selection=intervals, relative_freq=relative_freq, size=size, seed=seed,
                                          save_intent=False)
        interval_list = interval_tbl.columns.pop(0).to_pylist()
        interval_counts = pd.Series(interval_list, dtype='object').value_counts()
        rtn_list = []
        for index in interval_counts.index:
            size = interval_counts[index]
            if size == 0:
                continue
            if len(index) == 2:
                (lower, upper) = index
                if index == 0:
                    closed = 'both'
                else:
                    closed = 'right'
            else:
                (lower, upper, closed) = index
            if lower == upper:
                rtn_list += [round(lower, precision)] * size
                continue
            if precision == 0:
                margin = 1
            else:
                margin = 10 ** (((-1) * precision) - 1)
            if str.lower(closed) == 'neither':
                lower += margin
                upper -= margin
            elif str.lower(closed) == 'right':
                lower += margin
            elif str.lower(closed) == 'both':
                upper += margin
            # correct adjustments
            if lower >= upper:
                upper = lower + margin
            rtn_tbl = self.get_number(lower, upper, precision=precision, size=size, seed=seed, save_intent=False)
            rtn_list += rtn_tbl.columns.pop(0).to_pylist()
        np.random.default_rng(seed=seed).shuffle(rtn_list)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.StringArray.from_pandas(rtn_list)], names=[to_header]))

    def get_dist_normal(self, mean: float, std: float, canonical: pa.Table=None, precision: int=None, size: int=None,
                        quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                        intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """A normal (Gaussian) continuous random distribution.

        :param mean: The mean (“centre”) of the distribution.
        :param std: The standard deviation (jitter or “width”) of the distribution. Must be >= 0
        :param canonical: (optional) a pa.Table to append the result table to
        :param precision: The number of decimal points. The default is 3
        :param size: the size of the sample. if a tuple of intervals, size must match the tuple
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed() if seed is None else seed
        precision = precision if isinstance(precision, int) else 3
        generator = np.random.default_rng(seed=seed)
        rtn_list = list(generator.normal(loc=mean, scale=std, size=size))
        rtn_list = list(np.around(rtn_list, precision))
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_dist_choice(self, number: [int, str, float], canonical: pa.Table=None, size: int=None, quantity: float=None,
                        to_header: str=None,  seed: int=None, save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                        replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """Creates a list of latent values of 0 or 1 where 1 is randomly selected both upon the number given. The
        ``number`` parameter can be a direct reference to the canonical column header or to an environment variable.
        If the environment variable is used ``number`` should be set to ``"${<<YOUR_ENVIRON>>}"`` where
        <<YOUR_ENVIRON>> is the environment variable name

        :param number: The number of true (1) values to randomly chose from the canonical. see below
        :param canonical: (optional) a pa.Table to append the result table to
        :param size: the size of the sample. if a tuple of intervals, size must match the tuple
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                       If None: default's to -1
                       if -1: added to a level above any current instance of the intent section, level 0 if not found
                       if int: added to the level specified, overwriting any that already exist
        :param replace_intent: (optional) if the intent method exists at the level, or default level
                       True - replaces the current intent method with the new
                       False - leaves it untouched, disregarding the new intent
        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a list of 1 or 0

        as choice is a fixed value, number can be represented by an environment variable with the format '${NAME}'
        where NAME is the environment variable name
       """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed() if seed is None else seed
        number = self._extract_value(number)
        number = int(number * size) if isinstance(number, float) and 0 <= number <= 1 else int(number)
        number = number if 0 <= number < size else size
        if isinstance(number, int) and 0 <= number <= size:
            rtn_list = pd.Series(data=[0] * size)
            choice_tbl = self.get_number(stop=size, size=number, at_most=1, precision=0, ordered='asc', seed=seed,
                                         save_intent=False)
            choice_idx = choice_tbl.columns.pop(0).to_pylist()
            rtn_list.iloc[choice_idx] = [1] * number
            return rtn_list.reset_index(drop=True).to_list()
        rtn_list = pd.Series(data=[0] * size).to_list()
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_dist_bernoulli(self, probability: float, canonical: pa.Table=None, size: int=None, quantity: float=None,
                           to_header: str=None,  seed: int=None, save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                           replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """A Bernoulli discrete random distribution using scipy

        :param probability: the probability occurrence
        :param canonical: (optional) a pa.Table to append the result table to
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed() if seed is None else seed
        probability = self._extract_value(probability)
        rtn_list = list(stats.bernoulli.rvs(p=probability, size=size, random_state=seed))
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_dist_bounded_normal(self, mean: float, std: float, lower: float, upper: float, canonical: pa.Table=None,
                                precision: int=None, size: int=None, quantity: float=None, to_header: str=None,  seed: int=None,
                                save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                                replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """A bounded normal continuous random distribution.

        :param mean: the mean of the distribution
        :param std: the standard deviation
        :param lower: the lower limit of the distribution
        :param upper: the upper limit of the distribution
        :param canonical: (optional) a pa.Table to append the result table to
        :param precision: the precision of the returned number. if None then assumes int value else float
        :param size: the size of the sample
        :param quantity: a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: a seed value for the random function: default to None
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
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        precision = precision if isinstance(precision, int) else 3
        seed = self._seed() if seed is None else seed
        rtn_list = stats.truncnorm((lower - mean) / std, (upper - mean) / std, loc=mean, scale=std)
        rtn_list = rtn_list.rvs(size, random_state=seed).round(precision)
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_distribution(self, distribution: str, canonical: pa.Table=None, is_stats: bool=None, precision: int=None,
                         size: int=None, quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None,
                         intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                         remove_duplicates: bool=None, **kwargs) -> pa.Table:
        """returns a number based the distribution type.

        :param distribution: The string name of the distribution function from numpy random Generator class
        :param is_stats: (optional) if the generator is from the stats package and not numpy
        :param canonical: (optional) a pa.Table to append the result table to
        :param precision: (optional) the precision of the returned number
        :param size: (optional) the size of the sample
        :param quantity: (optional) a number between 0 and 1 representing data that isn't null
        :param to_header: (optional) an optional name to call the column
        :param seed: (optional) a seed value for the random function: default to None
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
        :param kwargs: the parameters of the method
        :return: a random number
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed() if seed is None else seed
        precision = 3 if precision is None else precision
        is_stats = is_stats if isinstance(is_stats, bool) else False
        if is_stats:
            rtn_list = eval(f"stats.{distribution}.rvs(size=size, random_state=_seed, **kwargs)", globals(), locals())
        else:
            generator = np.random.default_rng(seed=seed)
            rtn_list = eval(f"generator.{distribution}(size=size, **kwargs)", globals(), locals())
        rtn_list = list(np.around(rtn_list, precision))
        rtn_list = self._set_quantity(rtn_list, quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.NumericArray.from_pandas(rtn_list)], names=[to_header]))

    def get_string_pattern(self, pattern: str, canonical: pa.Table=None, choices: dict=None, as_binary: bool=None,
                           quantity: [float, int]=None, size: int=None, choice_only: bool=None, to_header: str=None,  seed: int=None,
                           save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                           replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ Returns a random string based on the pattern given. The pattern is made up from the choices passed but
        by default is as follows:
                - c = random char [a-z][A-Z]
                - d = digit [0-9]
                - l = lower case char [a-z]
                - U = upper case char [A-Z]
                - p = all punctuation
                - s = space

        you can also use punctuation in the pattern that will be retained
        A pattern example might be

        .. code:: text

                uuddsduu => BA12 2NE or dl-{uu} => 4g-{FY}

        to create your own choices pass a dictionary with a reference char key with a list of choices as a value

        :param pattern: the pattern to create the string from
        :param canonical: (optional) a pa.Table to append the result table to
        :param choices: (optional) an optional dictionary of list of choices to replace the default.
        :param as_binary: (optional) if the return string is prefixed with a b
        :param quantity: (optional) a number between 0 and 1 representing the percentage quantity of the data
        :param size: (optional) the size of the return list. if None returns a single value
        :param choice_only: (optional) if to only use the choices given or to take not found characters as is
        :param to_header: (optional) an optional name to call the column
        :param seed: (optional) a seed value for the random function: default to None
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
        :return: a string based on the pattern
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        choice_only = False if choice_only is None or not isinstance(choice_only, bool) else choice_only
        as_binary = as_binary if isinstance(as_binary, bool) else False
        quantity = self._quantity(quantity)
        seed = self._seed(seed=seed)
        if choices is None or not isinstance(choices, dict):
            choices = {'c': list(string.ascii_letters),
                       'd': list(string.digits),
                       'l': list(string.ascii_lowercase),
                       'U': list(string.ascii_uppercase),
                       'p': list(string.punctuation),
                       's': [' '],
                       }
            choices.update({p: [p] for p in list(string.punctuation)})
        else:
            for k, v in choices.items():
                if not isinstance(v, list):
                    raise ValueError(
                        "The key '{}' must contain a 'list' of replacements options. '{}' found".format(k, type(v)))

        generator = np.random.default_rng(seed=seed)
        rtn_list = pd.Series(dtype=str)
        for c in list(pattern):
            if c in choices.keys():
                result = generator.choice(choices[c], size=size)
            elif not choice_only:
                result = [c]*size
            else:
                continue
            s_result = pd.Series(result)
            if rtn_list.empty:
                rtn_list = s_result
            else:
                rtn_list += s_result
        if as_binary:
            rtn_list = rtn_list.str.encode(encoding='raw_unicode_escape')
        rtn_list = self._set_quantity(rtn_list.to_list(), quantity=self._quantity(quantity), seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.StringArray.from_pandas(rtn_list)], names=[to_header]))

    def get_sample(self, sample_name: str, canonical: pa.Table=None, sample_size: int=None, shuffle: bool=None,
                   size: int=None, quantity: float=None, to_header: str=None,  seed: int=None, save_intent: bool=None,
                   intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                   remove_duplicates: bool=None) -> pa.Table:
        """ returns a sample set based on sample_name. To see the potential samples call the property 'sample_list'.

        :param sample_name: The name of the Sample method to be used.
        :param canonical: (optional) a pa.Table to append the result table to
        :param sample_size: (optional) the size of the sample to take from the reference file
        :param shuffle: (optional) if the selection should be shuffled before selection. Default is true
        :param quantity: (optional) a number between 0 and 1 representing the percentage quantity of the data
        :param size: (optional) size of the return. default to 1
        :param to_header: (optional) an optional name to call the column
        :param seed: (optional) a seed value for the random function: default to None
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
        :return: a sample list
        """
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if sample_name not in self.sample_list:
            raise ValueError(f"The sample list '{sample_name}' does not exist as a sample list")
        sample_size = sample_size if isinstance(sample_size, int) else size
        quantity = self._quantity(quantity)
        seed = self._seed(seed=seed)
        shuffle = shuffle if isinstance(shuffle, bool) else True
        selection = eval(f"Sample.{sample_name}(size={size}, shuffle={shuffle}, seed={seed})")
        rtn_list = self._set_quantity(selection, quantity=quantity, seed=seed)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pa.Array.from_pandas(rtn_list)], names=[to_header]))

    def get_sample_map(self, sample_map: str, size: int, canonical: pa.Table=None, selection: list=None,
                       mask_null: bool=None, headers: [str, list]=None, shuffle: bool=None,
                       rename_columns: [dict, list]=None, seed: int=None, save_intent: bool=None,
                       column_name: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                       remove_duplicates: bool=None, **kwargs) -> pa.Table:
        """ returns a sample table based on sample_map. To see the potential samples call the property 'sample_map'.
        The returned table can be filtered by row (selection) or by column (headers)

        The selection is a list of triple tuples in the form: [(comparison, operation, logic)] where comparison
        is the item or column to compare, the operation is what to do when comparing and the logic if you are
        chaining tuples as in the logic to join to the next boolean flags to the current. An example might be:

                [(comparison, operation, logic)]
                [(1, 'greater', 'or'), (-1, 'less', None)]
                [(pa.array(['INACTIVE', 'PENDING']), 'is_in', None)]

        The operator and logic are taken from pyarrow.compute and are:

                operator => extract_regex, equal, greater, less, greater_equal, less_equal, not_equal, is_in, is_null
                logic => and, or, xor, and_not

                {header: [(comparison, operation, logic)]}

        :param sample_map: the sample map name.
        :param size: size of the return table.
        :param canonical: (optional) a pa.Table to append the result table to
        :param rename_columns: (optional) rename the returning sample columns with an exact list or replacement dict
        :param selection: (optional) a list of
        :param mask_null: (optional)
        :param headers: a header or list of headers to filter on
        :param shuffle: (optional) if the selection should be shuffled before selection. Default is true
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param column_name: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :param kwargs: any additional parameters to pass to the sample map
        :return: pa.Table
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   column_name=column_name, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        if sample_map not in self.sample_map:
            raise ValueError(f"The sample map '{sample_map}' does not exist as a sample maps")
        _seed = self._seed(seed=seed)
        shuffle = shuffle if isinstance(shuffle, bool) else True
        tbl = eval(f"MappedSample.{sample_map}(size={size}, shuffle={shuffle}, seed={_seed}, **{kwargs})")
        if isinstance(selection, dict):
            full_mask = pa.array([True]*tbl.num_rows)
            for header, condition in selection.items():
                mask = self._extract_mask(tbl.column(header), condition=condition, mask_null=mask_null)
                full_mask = pc.or_(full_mask, mask)
            tbl = tbl.filter(full_mask)
        if isinstance(rename_columns, dict):
            names = [rename_columns.get(item,item)  for item in tbl.column_names]
            tbl = tbl.rename_columns(names)
        if isinstance(rename_columns, list) and len(rename_columns) == tbl.num_columns:
            tbl = tbl.rename_columns(rename_columns)
        return Commons.table_append(canonical, tbl)

    def get_analysis(self, size: int, other: [str, pa.Table], canonical: pa.Table=None, category_limit: int=None,
                     date_jitter: int=None, date_units: str=None, date_ordered: bool=None, seed: int=None,
                     save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                     replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ builds a set of columns based on another (see analyse_association)
        if a reference DataFrame is passed then as the analysis is run if the column already exists the row
        value will be taken as the reference to the sub category and not the random value. This allows already
        constructed association to be used as reference for a sub category.

        :param size: The number of rows
        :param other: a direct or generated pd.DataFrame. see context notes below
        :param canonical: (optional) a pa.Table to append the result table to
        :param category_limit: (optional) a global cap on categories captured. zero value returns no limits
        :param date_jitter: (optional) The size of the jitter. Default to 2
        :param date_units: (optional) The date units. Options ['W', 'D', 'h', 'm', 's', 'milli', 'micro']. Default 'D'
        :param date_ordered: (optional) if the dates are shuffled or in order
        :param seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the column name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run. In
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
        # Code block for intent
        canonical = self._get_canonical(canonical)
        other = self._get_canonical(other)
        size = self._extract_value(size)
        if other is None or other.num_rows == 0:
            return None
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        date_jitter = date_jitter if isinstance(date_jitter, int) else 2
        units_allowed = ['W', 'D', 'h', 'm', 's', 'milli', 'micro']
        date_units = date_units if isinstance(date_units, str) and date_units in units_allowed else 'D'
        date_ordered = date_ordered if isinstance(date_ordered, bool) else False
        seed = self._seed(seed=seed)
        rtn_tbl = None
        gen = np.random.default_rng(seed)
        for c in other.column_names:
            column = other.column(c)
            if (pa.types.is_boolean(column.type) and pc.all(column).as_py() == False) or len(column.drop_null()) == 0:
                result = pa.table([pa.nulls(size)], names=[c])
                rtn_tbl = Commons.table_append(rtn_tbl, result)
                continue
            nulls = round(column.null_count / other.num_rows, 5)
            column = column.combine_chunks().drop_null()
            if pa.types.is_dictionary(column.type):
                selection = column.dictionary.to_pylist()
                frequency = column.value_counts().field(1).to_pylist()
                result = self.get_category(selection=selection, relative_freq=frequency, size=size, to_header=c,
                                           quantity=1-nulls, save_intent=False)
            elif pa.types.is_integer(column.type) or pa.types.is_floating(column.type):
                s_values = column.to_pandas()
                precision = 0 if pa.types.is_integer(column.type) else 5
                jitter = pc.round(pc.multiply(pc.stddev(column), 0.1), 5).as_py()
                result = s_values.add(gen.normal(loc=0, scale=jitter, size=s_values.size))
                while result.size < size:
                    _ = s_values.add(gen.normal(loc=0, scale=jitter, size=s_values.size))
                    result = pd.concat([result, _], axis=0)
                result = result.sample(frac=1).iloc[:size].astype(column.type.to_pandas_dtype()).reset_index(drop=True)
                result = self._set_quantity(result, quantity=self._quantity(1-nulls), seed=seed)
                result = pa.table([pa.Array.from_pandas(result)], names=[c])
            elif pa.types.is_boolean(column.type):
                frequency = dict(zip(column.value_counts().field(0).to_pylist(),
                                     column.value_counts().field(1).to_pylist())).get(True)
                if frequency is None:
                    frequency = 0
                prob = frequency/size
                prob = prob if 0 < prob < 1 else 0.5
                _ = gen.choice([True, False,], size=size, p=[prob, 1 - prob])
                result = self._set_quantity(_, quantity=self._quantity(1 - nulls), seed=seed)
                result = pa.table([pa.BinaryArray.from_pandas(result)], names=[c])
            elif pa.types.is_string(column.type):
                # for the moment do nothing with strings
                result = column.to_pandas()
                while result.size < size:
                    result = pd.concat([result, result], axis=0)
                result = result.sample(frac=1).iloc[:size].reset_index(drop=True)
                result = pd.Series(self._set_quantity(result, quantity=self._quantity(1-nulls), seed=seed))
                arr = pa.StringArray.from_pandas(result)
                result = pa.table([arr], names=[c])
            elif pa.types.is_date(column.type) or pa.types.is_timestamp(column.type):
                s_values = column.to_pandas()
                # set jitters to time deltas
                jitter = pd.Timedelta(value=date_jitter, unit=date_units) if isinstance(date_jitter, int) else pd.Timedelta(value=0)
                jitter = int(jitter.to_timedelta64().astype(int) / 10 ** 3)
                _ = gen.normal(loc=0, scale=jitter, size=s_values.size)
                _ = pd.Series(pd.to_timedelta(_, unit='micro'), index=s_values.index)
                result = s_values.add(_)
                while result.size < size:
                    _ = gen.normal(loc=0, scale=jitter, size=s_values.size)
                    _ = pd.Series(pd.to_timedelta(_, unit='micro'), index=s_values.index)
                    result = pd.concat([result, s_values.add(_)], axis=0)
                result = result.iloc[:size].astype(column.type.to_pandas_dtype())
                if date_ordered:
                    result = result.sample(frac=1).reset_index(drop=True)
                else:
                    result = result.sort_values(ascending=False).reset_index(drop=True)
                result = pd.Series(self._set_quantity(result, quantity=self._quantity(1-nulls), seed=seed))
                result = pa.table([pa.TimestampArray.from_pandas(result)], names=[c])
            else:
                # return nulls for other types
                result = pa.table([pa.nulls(size)], names=[c])
            rtn_tbl = Commons.table_append(rtn_tbl, result)
        return Commons.table_append(canonical, rtn_tbl)

    def get_synthetic_data_types(self, size: int, canonical: pa.Table=None, inc_nulls: bool=None,
                                 prob_nulls: float=None, seed: int=None, category_encode: bool=None,
                                 save_intent: bool=None, intent_level: [int, str]=None,intent_order: int=None,
                                 replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ A dataset with example data types

        :param size: The size of the sample
        :param inc_nulls: include values with nulls
        :param canonical: (optional) a pa.Table to append the result table to
        :param prob_nulls: (optional) a value between 0 an 1 of the percentage of nulls. Default 0.02
        :param category_encode: (optional) if the categorical should be encoded to DictionaryArray
        :param seed: (optional) a seed value for the random function: default to None
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
        :return: pandas DataSet
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed(seed=seed)
        prob_nulls = prob_nulls if isinstance(prob_nulls, float) and 0 < prob_nulls < 1 else 0.1
        category_encode = category_encode if isinstance(category_encode, bool) else True
        # cat
        canonical = self.get_category(selection=['SUSPENDED', 'ACTIVE', 'PENDING', 'INACTIVE', 'ARCHIVE'],
                                      canonical=canonical, size=size, seed=seed, relative_freq=[1, 70, 20, 30, 10],
                                      encode=category_encode, to_header='cat', save_intent=False)
        # num
        canonical = self.get_dist_normal(mean=0, std=1, canonical=canonical, size=size, seed=seed, to_header='num',
                                         save_intent=False)
        canonical = self.correlate_number(canonical, 'num', precision=5, jitter=2, seed=seed, to_header='num',
                                          save_intent=False)
        # int
        canonical = self.get_number(start=size, stop=size * 10, at_most=1, ordered=True, canonical=canonical, size=size,
                                    seed=seed, to_header='int', save_intent=False)
        # bool
        canonical = self.get_boolean(size=size, probability=0.7, canonical=canonical, seed=seed, to_header='bool',
                                     save_intent=False)
        # date
        canonical = self.get_datetime(start='2022-12-01', until='2023-03-31', ordered=True, canonical=canonical,
                                      size=size, seed=seed, to_header='date', save_intent=False)
        # string
        canonical = self.get_sample(sample_name='us_street_names', canonical=canonical, size=size, seed=seed,
                                    to_header='string',  save_intent=False)

        if isinstance(inc_nulls, bool) and inc_nulls:
            gen = np.random.default_rng()
            # cat_null
            prob_nulls = (gen.integers(1, 10, 1) * 0.001)[0] + prob_nulls
            canonical = self.get_category(selection=['High', 'Med', 'Low'], canonical=canonical, relative_freq=[9,8,4],
                                          quantity=1 - prob_nulls, to_header='cat_null', size=size,
                                          encode=category_encode, seed=seed, save_intent=False)
            # num_null
            prob_nulls = (gen.integers(1, 10, 1) * 0.001)[0] + prob_nulls
            canonical = self.get_number(start=-1.0, stop=1.0, canonical=canonical, size=size,
                                        relative_freq=[1, 1, 2, 3, 5, 8, 13, 21], quantity=1 - prob_nulls,
                                        to_header='num_null', seed=seed, save_intent=False)
            # date_null
            prob_nulls = (gen.integers(1, 10, 1) * 0.001)[0] + prob_nulls
            canonical = self.get_datetime(start='2023-02-01', until='2023-05-31', canonical=canonical, ordered=True,
                                          size=size, quantity=1 - prob_nulls, to_header='date_null', seed=seed,
                                          save_intent=False)
            # string_null
            prob_nulls = (gen.integers(1, 10, 1) * 0.001)[0] + prob_nulls
            canonical = self.get_sample(sample_name='us_cities', canonical=canonical, size=size, quantity=1-prob_nulls,
                                        to_header='string_null', seed=seed, save_intent=False)
            #sparse
            canonical = self.get_number(start=-50, stop=8.0, canonical=canonical, size=size, quantity=0.3,
                                        to_header='sparse', seed=seed, save_intent=False)
            # one string
            _ = pa.table([pa.array(['one']*size)], names=['one_string'])
            canonical = Commons.table_append(canonical, _)
            # duplicate num
            _ = pa.table([canonical.column('num')], names=['dup_num'])
            canonical = Commons.table_append(canonical, _)
            # nulls_int
            _ = pa.table([pa.array(pa.nulls(size), pa.int64())], names=['nulls_int'])
            canonical = Commons.table_append(canonical, _)
            # nulls_date
            _ = pa.table([pa.array(pa.nulls(size), pa.timestamp('ns'))], names=['nulls_date'])
            canonical = Commons.table_append(canonical, _)
            # nulls_str
            _ = pa.table([pa.array(pa.nulls(size), pa.string())], names=['nulls_str'])
            canonical = Commons.table_append(canonical, _)
            # nulls
            _ = pa.table([pa.nulls(size)], names=['nulls'])
            canonical = Commons.table_append(canonical, _)
            # binary
            canonical = self.get_string_pattern(pattern='cccccccc', canonical=canonical, as_binary=True, size=size,
                                                seed=seed, to_header='binary', save_intent=False)
            # list array
            _ = pa.array(list(zip(canonical.column('num').to_pylist(), canonical.column('num_null').to_pylist())))
            _ = pa.table([_], names=['nest_list'])
            canonical = Commons.table_append(canonical, _.slice(0, size))

        return canonical

    def get_noise(self, size: int, num_columns: int, canonical: pa.Table=None, seed: int=None, name_prefix: str=None,
                  save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                  replace_intent: bool=None, remove_duplicates: bool=None) -> pd.DataFrame:
        """ Generates multiple columns of noise in your dataset

        :param size: The number of rows
        :param num_columns: the number of columns of noise
        :param canonical: (optional) a pa.Table to append the result table to
        :param name_prefix: a name the prefix the column names
        :param seed: seed: (optional) a seed value for the random function: default to None
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
        :return: a DataFrame
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # Code block for intent
        canonical = self._get_canonical(canonical)
        size = self._extract_value(size)
        if not isinstance(size, int):
            raise ValueError("size not set. Size must be an int greater than zero")
        seed = self._seed(seed=seed)
        num_columns = num_columns if isinstance(num_columns, int) else 1
        name_prefix = name_prefix if isinstance(name_prefix, str) else ''
        label_gen = Commons.label_gen()
        rtn_tbl = None
        generator = np.random.default_rng(seed=seed)
        for _ in range(num_columns):
            seed = self._seed(seed=seed, increment=True)
            a = generator.choice(range(1, 6))
            b = generator.choice(range(1, 6))
            _ = self.get_distribution(distribution='beta', a=a, b=b, precision=6, size=size, seed=seed,
                                      to_header=f"{name_prefix}{next(label_gen)}", save_intent=False)
            rtn_tbl = Commons.table_append(rtn_tbl, _)
        return Commons.table_append(canonical, rtn_tbl)

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

    def correlate_dates(self, canonical: pa.Table, header: str, choice: [int, float, str]=None, choice_header: str=None,
                        offset: [int, dict, str]=None, jitter: [int, str]=None, jitter_units: str=None,
                        ignore_time: bool=None, ignore_seconds: bool=None, min_date: str=None, max_date: str=None,
                        now_delta: str=None, to_header: str=None, date_format: str=None, day_first: bool=None,
                        year_first: bool=None, seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                        intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None):
        """ correlate a list of continuous dates adjusting those dates, or a subset of those dates, with a
        normalised jitter along with a value offset. ``choice``, ``jitter`` and ``offset`` can accept environment
        variable string names starting with ``${`` and ending with ``}``.

        When using offset and a dict is passed, the dict should take the form {'days': 1}, where the unit is plural,
        to add 1 day or a singular name {'hour': 3}, where the unit is singular, to replace the current with 3 hours.
        Offsets can be 'years', 'months', 'weeks', 'days', 'hours', 'minutes' or 'seconds'. If an int is passed
        days are assumed.

        :param canonical: a pd.DataFrame as the reference dataframe
        :param header: the header in the DataFrame to correlate
        :param choice: (optional) The number of values or percentage between 0 and 1 to choose.
        :param choice_header: (optional) those not chosen are given the values of the given header
        :param offset: (optional) Temporal parameter that add to or replace the offset value. if int then assume 'days'
        :param jitter: (optional) the random jitter or deviation in days
        :param jitter_units: (optional) the units of the jitter, Options: 'W', 'D', 'h', 'm', 's'. default 'D'
        :param to_header: (optional) an optional name to call the column
        :param ignore_time: ignore time elements and only select from Year, Month, Day elements. Default is False
        :param ignore_seconds: ignore second elements and only select from Year to minute elements. Default is False
        :param min_date: (optional)a minimum date not to go below
        :param max_date: (optional)a max date not to go above
        :param now_delta: (optional) returns a delta from now as an int list, Options: 'Y', 'M', 'W', 'D', 'h', 'm', 's'
        :param day_first: (optional) if the dates given are day first firmat. Default to True
        :param year_first: (optional) if the dates given are year first. Default to False
        :param date_format: (optional) the format of the output
        :param seed: (optional) a seed value for the random function: default to None
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
        :return: a list of equal size to that given
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
        values = canonical.column(header).to_pandas()
        choice_header = choice_header if isinstance(choice_header, str) and choice_header in canonical.column_names else header
        others = canonical.column(choice_header).to_pandas()

        def _clean(control):
            _unit_type = ['years', 'months', 'weeks', 'days', 'hours', 'minutes', 'seconds',
                          'year', 'month', 'week', 'day', 'hour', 'minute', 'second']
            _params = {}
            if isinstance(control, int):
                control = {'days': control}
            if isinstance(control, dict):
                for k, v in control.items():
                    if k not in _unit_type:
                        raise ValueError(f"The key '{k}' in 'offset', is not a recognised unit type for pd.DateOffset")
            return control

        seed = self._seed() if seed is None else seed
        ignore_seconds = ignore_seconds if isinstance(ignore_seconds, bool) else False
        ignore_time = ignore_time if isinstance(ignore_time, bool) else False
        offset = _clean(offset) if isinstance(offset, (dict, int)) else None
        if isinstance(now_delta, str) and now_delta not in ['Y', 'M', 'W', 'D', 'h', 'm', 's']:
            raise ValueError(f"the now_delta offset unit '{now_delta}' is not recognised "
                             f"use of of ['Y', 'M', 'W', 'D', 'h', 'm', 's']")
        # set minimum date
        _min_date = pd.to_datetime(min_date, errors='coerce')
        if _min_date is None or _min_date is pd.NaT:
            _min_date = pd.to_datetime(pd.Timestamp.min)
        # set max date
        _max_date = pd.to_datetime(max_date, errors='coerce')
        if _max_date is None or _max_date is pd.NaT:
            _max_date = pd.to_datetime(pd.Timestamp.max)
        if _min_date >= _max_date:
            raise ValueError(f"the min_date {min_date} must be less than max_date {max_date}")
        # convert values into datetime
        s_values = pd.Series(pd.to_datetime(values, errors='coerce', dayfirst=day_first, yearfirst=year_first))
        s_others = pd.Series(pd.to_datetime(others, errors='coerce', dayfirst=day_first, yearfirst=year_first))
        dt_tz = s_values.dt.tz
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
        if isinstance(jitter, (str, int)):
            size = s_values.size
            jitter = self._extract_value(jitter)
            jitter_units = self._extract_value(jitter_units)
            units_allowed = ['W', 'D', 'h', 'm', 's', 'milli', 'micro']
            jitter_units = jitter_units if isinstance(jitter_units, str) and jitter_units in units_allowed else 'D'
            # set jitters to time deltas
            jitter = pd.Timedelta(value=jitter, unit=jitter_units) if isinstance(jitter, int) else pd.Timedelta(value=0)
            jitter = int(jitter.to_timedelta64().astype(int) / 10 ** 3)
            gen = np.random.default_rng(seed)
            results = gen.normal(loc=0, scale=jitter, size=size)
            results = pd.Series(pd.to_timedelta(results, unit='micro'), index=s_values.index)
            s_values = s_values.add(results)
        null_idx = s_values[s_values.isna()].index
        if isinstance(offset, dict) and offset:
            s_values = s_values.add(pd.DateOffset(**offset))
        # sort max and min
        if _min_date > pd.to_datetime(pd.Timestamp.min):
            if _min_date > s_values.min():
                min_idx = s_values.dropna().where(s_values < _min_date).dropna().index
                s_values.iloc[min_idx] = _min_date
            else:
                raise ValueError(f"The min value {min_date} is greater than the max result value {s_values.max()}")
        if _max_date < pd.to_datetime(pd.Timestamp.max):
            if _max_date < s_values.max():
                max_idx = s_values.dropna().where(s_values > _max_date).dropna().index
                s_values.iloc[max_idx] = _max_date
            else:
                raise ValueError(f"The max value {max_date} is less than the min result value {s_values.min()}")
        # set the changed values
        if canonical.num_rows == s_values.size:
            s_others = s_values
        else:
            s_others.iloc[s_values.index] = s_values
        if now_delta:
            s_others = s_others.dt.tz_convert(None) if s_others.dt.tz else s_others
            s_others = (s_others - pd.Timestamp.now()).abs()
            s_others = (s_others / np.timedelta64(1, now_delta))
            s_others = s_others.round(0) if null_idx.size > 0 else s_others.astype(int)
        else:
            if isinstance(date_format, str):
                s_others = s_others.dt.strftime(date_format)
            else:
                if s_others.dt.tz:
                    s_others = s_others.dt.tz_convert(dt_tz)
                else:
                    s_others = s_others.dt.tz_localize(dt_tz)
        if ignore_time:
            s_others = pd.Series(pd.DatetimeIndex(s_others).normalize())
        elif ignore_seconds:
            s_others = s_others.dt.round('min')
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([s_others], names=[to_header]))

    def correlate_date_diff(self, canonical: pa.Table, first_date: str, second_date: str, units: str=None,
                            to_header: str=None, precision: int=None, seed: int=None, save_intent: bool=None,
                            intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                            remove_duplicates: bool=None, **kwargs):
        """ returns a column for the difference between a primary and secondary date where the primary is an early date
        than the secondary.

        :param canonical:
        :param first_date: the primary or older date field
        :param second_date: the secondary or newer date field
        :param units: (optional) The Timedelta units e.g. 'us', 'ms', 's', 'm', 'h', 'D', 'W', 'M', 'Y'. default is 'D'
        :param to_header: (optional) an optional name to call the column
        :param precision: the precision of the result
        :param seed: (optional) a seed value for the random function: default to None
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
        :param kwargs: a set of kwargs to include in any executable function
        :return: value set based on the selection list and the action
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        if second_date not in canonical.column_names:
            raise ValueError(f"The column header '{second_date}' is not in the canonical DataFrame")
        if first_date not in canonical.column_names:
            raise ValueError(f"The column header '{first_date}' is not in the canonical DataFrame")
        canonical = self._get_canonical(canonical)
        _seed = seed if isinstance(seed, int) else self._seed()
        precision = precision if isinstance(precision, int) else 0
        units = units if isinstance(units, str) else 'D'
        selected = Commons.filter_columns(canonical, headers=[first_date, second_date]).to_pandas()
        rename = (selected[second_date].sub(selected[first_date], axis=0) / np.timedelta64(1, units))
        rtn_arr = pa.array([np.round(v, precision) for v in rename], pa.int64())
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
        rtn_arr = DataDiscovery.to_discrete_intervals(column=canonical.column(header), granularity=granularity,
                                                      lower=lower, upper=upper, categories=categories,
                                                      precision=precision)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([rtn_arr.dictionary_encode()], names=[to_header]))

    def correlate_on_condition(self, canonical: pa.Table, header: str, other: str, condition: list,
                               value: [int, float, bool, str], mask_null: bool=None,
                               default: [int, float, bool, str]=None, to_header: str=None, seed: int=None,
                               save_intent: bool=None, intent_order: int=None, intent_level: [int, str]=None,
                               replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ correlates a named header to other header where the condition is met and replaces the header column
        value with a constant or value at the same index of an array.

        The selection is a list of triple tuples in the form: [(comparison, operation, logic)] where comparison
        is the item or column to compare, the operation is what to do when comparing and the logic if you are
        chaining tuples as in the logic to join to the next boolean flags to the current. An example might be:

                [(comparison, operation, logic)]
                [(1, 'greater', 'or'), (-1, 'less', None)]
                [(pa.array(['INACTIVE', 'PENDING']), 'is_in', None)]

        The operator and logic are taken from pyarrow.compute and are:

                operator => extract_regex, equal, greater, less, greater_equal, less_equal, not_equal, is_in, is_null
                logic => and, or, xor, and_not

        :param canonical: a pa.Table as the reference table
        :param header: the header for the target values to change
        :param other: the other header to correlate
        :param condition: a tuple or tuples of
        :param value: a constant value. If the value is a string starting @ then a header values are taken
        :param default: (optional) a default constant if not value. A string starting @ then a default name is taken
        :param to_header: (optional) an optional name to call the column
        :param mask_null: (optional) if nulls in the other they require a value representation.
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
        _mask = self._extract_mask(o_col, condition=condition, mask_null=mask_null)
        # check the value
        if isinstance(value, str) and value.startswith('@'):
            value = canonical.column(value[1:]).combine_chunks()
        if isinstance(default, str) and default.startswith('@'):
            default = canonical.column(default[1:]).combine_chunks()
        elif default is None:
            default = h_col
            # replace and add it back to the original table
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([pc.if_else(_mask, value, default)], names=[to_header]))

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

    def correlate_custom(self, canonical: pa.Table, code_str: str, seed: int=None, to_header: str=None,
                         save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                         replace_intent: bool=None, remove_duplicates: bool=None, **kwargs):
        """ Commonly used for custom list comprehension, takes code string that when evaluated returns a list of values
        Before using this method, consider the method correlate_selection(...)

        When referencing the canonical in the code_str it should be referenced either by use parameter label 'canonical'
        or the short cut '@' symbol.
        for example:

        .. code-block:: py3

            code_str = "[x + 2 for x in @['A']]" # where 'A' is a header in the canonical

        kwargs can also be passed into the code string but must be preceded by a '$' symbol
        for example:

        .. code-block:: py3

            code_str = "[True if x == $v1 else False for x in @['A']]" # where 'v1' is a kwargs

        :param canonical:
        :param code_str: an action on those column values. to reference the canonical use '@'
        :param to_header: (optional) an optional name to call the column
        :param seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :param kwargs: a set of kwargs to include in any executable function
        :return: value set based on the selection list and the action
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   Intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        _seed = seed if isinstance(seed, int) else self._seed()
        local_kwargs = locals()
        for k, v in local_kwargs.pop('kwargs', {}).items():
            local_kwargs.update({k: v})
            code_str = code_str.replace(f'${k}', str(v))
        code_str = code_str.replace('@', 'canonical')
        rtn_values = eval(code_str, globals(), local_kwargs)
        to_header = to_header if isinstance(to_header, str) else next(self.label_gen)
        return Commons.table_append(canonical, pa.table([rtn_values], names=[to_header]))

    def model_sample_link(self, canonical: pa.Table, other: [str, pa.Table], headers: list, replace: bool=None,
                          rename_map: [dict, list]=None, multi_map: dict=None, relative_freq: list=None, seed: int=None,
                          save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                          replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ Takes a target dataset and samples from that target to the size of the canonical

        :param canonical: a pa.Table as the reference table
        :param other: a direct pa.Table or reference to a connector.
        :param headers: the headers to be selected from the other table
        :param rename_map: (optional) a direct (list) or named (dict) mapping to the headers names.
        :param multi_map: (optional) multiple columns from a single e.g. {new_name: name} where name is copied new_name
        :param replace: (optional) assuming other is bigger than canonical, selects without replacement when True
        :param relative_freq: (optional) a weighting pattern of the selected data
        :param seed: (optional) a seed value for the random function: default to None
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
        headers = Commons.list_formatter(headers)
        replace = replace if isinstance(replace, bool) else True
        seed = self._seed() if seed is None else seed
        # build the distribution sizes
        if isinstance(relative_freq, list) and len(relative_freq) > 1:
            relative_freq = self._freq_dist_size(relative_freq=relative_freq, size=other.num_rows, seed=seed)
        else:
            relative_freq = None
        other = Commons.filter_columns(other, headers=headers).to_pandas()
        other = other.sample(n=canonical.num_rows, weights=relative_freq, random_state=seed, ignore_index=True,
                             replace=replace)
        if isinstance(rename_map, list) and len(rename_map) == len(headers):
            other.columns = rename_map
        elif isinstance(rename_map, dict):
            other.rename(mapper=rename_map, axis='columns', inplace=True)
        if isinstance(multi_map, dict):
            for k, v in multi_map.items():
                if v in other.columns:
                    other[k] = other[v]
        other = pa.Table.from_pandas(other)
        return Commons.table_append(canonical, other)

    def model_missing(self, canonical: pa.Table, strategy: str=None, headers: [str, list]=None,
                      d_types: [str, list]=None, regex: [str, list]=None, drop: bool=None, seed: int=None,
                      save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                      replace_intent: bool=None, remove_duplicates: bool=None) -> pa.Table:
        """ Imputes missing data with a probabilistic value based on the data pattern and the surrounding values.
        Can be applied to any type. This is the default.

        :param canonical:
        :param strategy: (optional) replace null. By default, probability, or mean, medium, mode, forward, backward
        :param headers: (optional) a filter of headers from the 'other' dataset
        :param drop: (optional) to drop or not drop the headers if specified
        :param d_types: (optional) a filter on data type for the 'other' dataset. int, float, bool, object
        :param regex: (optional) a regular expression to search the headers. example '^((?!_amt).)*$)' excludes '_amt'
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
        _seed = self._seed() if seed is None else seed
        strategy = strategy if isinstance(strategy, str) else 'probability'
        tbl = Commons.filter_columns(canonical, headers=headers, d_types=d_types, regex=regex, drop=drop)
        if tbl.num_columns == 0:
            return canonical
        rtn_tbl = None
        for n in tbl.column_names:
            c = tbl.column(n).combine_chunks()
            if pa.types.is_integer(c.type) or pa.types.is_floating(c.type):
                precision = Commons.column_precision(c)
                if strategy == 'mean':
                    c = c.fill_null(pc.round(pc.mean(c), precision))
                elif strategy == 'median':
                    c = c.fill_null(pc.round(pc.approximate_median(c), precision))
                elif strategy == 'mode':
                    c = c.fill_null(pc.round(pc.mode(c), precision))
                elif strategy == 'knn_uniform' or strategy == 'knn_distance':
                    weights = strategy[4:]
                    model = KNNImputer(n_neighbors=5, weights=weights)
                    np_array = c.to_pandas().to_numpy().reshape(-1, 1)
                    c = pa.Array.from_pandas(model.fit_transform(np_array).reshape(1, -1)[0])
            if strategy == 'forward':
                c = pc.fill_null_forward(c)
            elif strategy == 'backward':
                c = c.fill_null_backward(c)
            else:
                # get the analysis
                anal_tbl = self.get_analysis(tbl.num_rows, pa.table([c.drop_null()], names=[n]))
                c = c.fill_null(anal_tbl.column(n))
            rtn_tbl = Commons.table_append(rtn_tbl, pa.table([c], names=[n]))
        return Commons.table_append(canonical, rtn_tbl)

    def model_group(self, canonical: Any, group_by: [str, list], headers: [str, list]=None, regex: bool=None,
                    aggregator: str=None, list_choice: int=None, list_max: int=None, drop_group_by: bool = False,
                    seed: int=None, include_weighting: bool = False, freq_precision: int=None,
                    remove_weighting_zeros: bool = False, remove_aggregated: bool = False, save_intent: bool=None,
                    intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                    remove_duplicates: bool=None) -> pd.DataFrame:
        """ returns the full column values directly from another connector data source. in addition the the
        standard groupby aggregators there is also 'list' and 'set' that returns an aggregated list or set.
        These can be using in conjunction with 'list_choice' and 'list_size' allows control of the return values.
        if list_max is set to 1 then a single value is returned rather than a list of size 1.

        :param canonical: a direct or generated pd.DataFrame. see context notes below
        :param headers: the column headers to apply the aggregation too
        :param group_by: the column headers to group by
        :param regex: if the column headers is q regex
        :param aggregator: (optional) the aggregator as a function of Pandas DataFrame 'groupby' or 'list' or 'set'
        :param list_choice: (optional) used in conjunction with list or set aggregator to return a random n choice
        :param list_max: (optional) used in conjunction with list or set aggregator restricts the list to a n size
        :param drop_group_by: (optional) drops the group by headers
        :param include_weighting: (optional) include a percentage weighting column for each
        :param freq_precision: (optional) a precision for the relative_freq values
        :param remove_aggregated: (optional) if used in conjunction with the weighting then drops the aggrigator column
        :param remove_weighting_zeros: (optional) removes zero values
        :param seed: (optional) this is a place holder, here for compatibility across methods
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a pd.DataFrame
        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        _seed = self._seed() if seed is None else seed
        generator = np.random.default_rng(seed=_seed)
        freq_precision = freq_precision if isinstance(freq_precision, int) else 3
        aggregator = aggregator if isinstance(aggregator, str) else 'sum'
        headers = Commons.filter_headers(canonical, regex=headers) if isinstance(regex, bool) and regex else None
        headers = Commons.list_formatter(headers) if isinstance(headers, (list,str)) else canonical.column_names
        group_by = Commons.list_formatter(group_by)
        tbl_sub = Commons.filter_columns(canonical, headers=headers + group_by).drop_null()
        df_sub = tbl_sub.to_pandas()
        if aggregator.startswith('set') or aggregator.startswith('list'):
            df_tmp = df_sub.groupby(group_by)[headers[0]].apply(eval(aggregator)).apply(lambda x: list(x))
            df_tmp = df_tmp.reset_index()
            for idx in range(1, len(headers)):
                result = df_sub.groupby(group_by)[headers[idx]].apply(eval(aggregator)).apply(lambda x: list(x))
                df_tmp = df_tmp.merge(result, how='left', left_on=group_by, right_index=True)
            for idx in range(len(headers)):
                header = headers[idx]
                if isinstance(list_choice, int):
                    df_tmp[header] = df_tmp[header].apply(lambda x: generator.choice(x, size=list_choice))
                if isinstance(list_max, int):
                    df_tmp[header] = df_tmp[header].apply(lambda x: x[0] if list_max == 1 else x[:list_max])
            df_sub = df_tmp
        else:
            df_sub = df_sub.groupby(group_by, as_index=False).agg(aggregator)
        if include_weighting:
            df_sub['sum'] = df_sub.sum(axis=1, numeric_only=True)
            total = df_sub['sum'].sum()
            df_sub['weighting'] = df_sub['sum'].\
                apply(lambda x: round((x / total), freq_precision) if isinstance(x, (int, float)) else 0)
            df_sub = df_sub.drop(columns='sum')
            if remove_weighting_zeros:
                df_sub = df_sub[df_sub['weighting'] > 0]
            df_sub = df_sub.sort_values(by='weighting', ascending=False)
        if remove_aggregated:
            df_sub = df_sub.drop(headers, axis=1)
        if drop_group_by:
            df_sub = df_sub.drop(columns=group_by, errors='ignore')
        return pa.Table.from_pandas(df_sub)

    def model_merge(self, canonical: Any, other: Any, left_on: str=None, right_on: str=None, on: str=None,
                    how: str=None, headers: list=None, suffixes: tuple=None, indicator: bool=None,
                    validate: str=None,
                    replace_nulls: bool=None, seed: int=None, save_intent: bool=None,
                    intent_level: [int, str]=None,
                    intent_order: int=None, replace_intent: bool=None,
                    remove_duplicates: bool=None) -> pd.DataFrame:
        """ returns the full column values directly from another connector data source.

        :param canonical: a direct or generated pd.DataFrame. see context notes below
        :param other: a direct or generated pd.DataFrame. see context notes below
        :param left_on: the canonical key column(s) to join on
        :param right_on: the merging dataset key column(s) to join on
        :param on: if th left and right join have the same header name this can replace left_on and right_on
        :param how: (optional) One of 'left', 'right', 'outer', 'inner'. Defaults to inner. See below for more detailed
                    description of each method.
        :param headers: (optional) a filter on the headers included from the right side
        :param suffixes: (optional) A tuple of string suffixes to apply to overlapping columns. Defaults ('', '_dup').
        :param indicator: (optional) Add a column to the output DataFrame called _merge with information on the source
                    of each row. _merge is Categorical-type and takes on a value of left_only for observations whose
                    merge key only appears in 'left' DataFrame or Series, right_only for observations whose merge key
                    only appears in 'right' DataFrame or Series, and both if the observation’s merge key is found
                    in both.
        :param validate: (optional) validate : string, default None. If specified, checks if merge is of specified type.
                            “one_to_one” or “1:1”: checks if merge keys are unique in both left and right datasets.
                            “one_to_many” or “1:m”: checks if merge keys are unique in left dataset.
                            “many_to_one” or “m:1”: checks if merge keys are unique in right dataset.
                            “many_to_many” or “m:m”: allowed, but does not result in checks.
        :param replace_nulls: (optional) replaces nulls with an appropriate value dependent upon the field type
        :param seed: this is a placeholder, here for compatibility across methods
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent name that groups intent to create a column
        :param intent_order: (optional) the order in which each intent should run.
                    - If None: default's to -1
                    - if -1: added to a level above any current instance of the intent section, level 0 if not found
                    - if int: added to the level specified, overwriting any that already exist

        :param replace_intent: (optional) if the intent method exists at the level, or default level
                    - True - replaces the current intent method with the new
                    - False - leaves it untouched, disregarding the new intent

        :param remove_duplicates: (optional) removes any duplicate intent in any level that is identical
        :return: a pd.DataFrame

        The other is a pd.DataFrame, a pd.Series or list, a connector contract str reference or a set of
        parameter instructions on how to generate a pd.Dataframe. the description of each is:

        - pd.Dataframe -> a deep copy of the pd.DataFrame
        - pd.Series or list -> creates a pd.DataFrame of one column with the 'header' name or 'default' if not given
        - str -> instantiates a connector handler with the connector_name and loads the DataFrame from the connection
        - dict -> use canonical2dict(...) to help construct a dict with a 'method' to build a pd.DataFrame
            methods:
                - model_*(...) -> one of the SyntheticBuilder model methods and parameters
                - @empty -> generates an empty pd.DataFrame where size and headers can be passed
                    :size sets the index size of the dataframe
                    :headers any initial headers for the dataframe
                - @generate -> generate a synthetic file from a remote Domain Contract
                    :task_name the name of the SyntheticBuilder task to run
                    :repo_uri the location of the Domain Product
                    :size (optional) a size to generate
                    :seed (optional) if a seed should be applied
                    :run_book (optional) if specific intent should be run only

        """
        # intent persist options
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # remove intent params
        canonical = self._get_canonical(canonical)
        other = self._get_canonical(other).slice(0, canonical.num_rows)
        _seed = self._seed() if seed is None else seed
        how = how if isinstance(how, str) and how in ['left', 'right', 'outer', 'inner'] else 'inner'
        indicator = indicator if isinstance(indicator, bool) else False
        suffixes = suffixes if isinstance(suffixes, tuple) and len(suffixes) == 2 else ('', '_dup')
        # Filter on the columns
        df = canonical.to_pandas()
        df_other = other.to_pandas()
        if isinstance(headers, list):
            headers.append(right_on if isinstance(right_on, str) else on)
            other = Commons.filter_columns(other, headers=headers)
        df_rtn = df.merge(right=df_other, how=how, left_on=left_on, right_on=right_on, on=on, suffixes=suffixes,
                          indicator=indicator, validate=validate)
        return pa.Table.from_pandas(df_rtn)
