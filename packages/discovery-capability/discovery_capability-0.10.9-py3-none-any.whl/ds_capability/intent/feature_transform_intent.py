import inspect
import numpy as np
import pandas as pd
import pyarrow as pa
import pyarrow.compute as pc
from scipy.stats import stats

from ds_capability.components.commons import Commons
from ds_capability.intent.common_intent import CommonsIntentModel
from ds_capability.intent.abstract_feature_transform_intent import AbstractFeatureTransformIntentModel


class FeatureTransformIntent(AbstractFeatureTransformIntentModel, CommonsIntentModel):

    def encode_date_integer(self, canonical: pa.Table, headers: [str, list]=None, prefix=None, day_first: bool = True,
                            year_first: bool = False, seed: int=None, save_intent: bool=None,
                            intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                            remove_duplicates: bool=None):
        """ date encoding to integer replaces dates for integer values.

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply encoding too
        :param prefix: (optional) a str to prefix the column
        :param day_first: (optional) if the dates given are day first format. Default to True
        :param year_first: (optional) if the dates given are year first. Default to False
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        prefix = prefix if isinstance(prefix, str) else ''
        headers = Commons.list_formatter(headers) if isinstance(headers,(str, list)) else canonical.column_names
        _ = self._seed() if seed is None else seed
        tbl = None
        for n in headers:
            c = canonical.column(n).combine_chunks()
            if not (pa.types.is_timestamp(c.type) or pa.types.is_time(c.type)):
                continue
            column = pa.array(Commons.date2value(c.to_pylist()), pa.int64())
            new_header = f"{prefix}{n}"
            tbl = Commons.table_append(tbl, pa.table([column], names=[new_header]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)

    def encode_category_integer(self, canonical: pa.Table, headers: [str, list]=None, ranking: list=None, prefix=None,
                                seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                                intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None):
        """ Integer encoding replaces the categories by digits from 1 to n, where n is the number of distinct
        categories of the variable. Integer encoding can be either nominal or ordinal.

        Nominal data is categorical variables without any particular order between categories. This means that
        the categories cannot be sorted and there is no natural order between them.

        Ordinal data represents categories with a natural, ordered relationship between each category. This means
        that the categories can be sorted in either ascending or descending order. In order to encode integers as
        ordinal, a ranking must be provided.

        If ranking is given, the return will be ordinal values based on the ranking order of the list. If a
        categorical value is not found in the list it is grouped with other missing values and given the last
        ranking.

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply encoding too
        :param ranking: (optional) if used, ranks the categorical values to the list given
        :param prefix: a str to prefix the column
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        prefix = prefix if isinstance(prefix, str) else ''
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _ = self._seed() if seed is None else seed
        tbl = None
        for header in headers:
            column = canonical.column(header).combine_chunks()
            if isinstance(ranking, list): # ordinal
                if pa.types.is_dictionary(column.type):
                    column = column.dictionary_decode()
                rank = Commons.list_formatter(ranking)
                unique = pc.unique(column).to_pylist()
                missing = Commons.list_diff(unique, rank, symmetric=False)
                full_rank = rank + missing
                values = list(range(len(rank)))
                values = values + ([len(rank)] * (len(full_rank) - len(rank)))
                mapper = dict(zip(full_rank, values))
                s_column = column.to_pandas()
                column =  pa.Array.from_pandas(self, s_column.replace(mapper))
            else: # nominal
                if not pa.types.is_dictionary(column.type):
                    column = column.dictionary_encode()
                column = pa.array(column.indicies, pa.int64())
            new_header = f"{prefix}{header}"
            tbl = Commons.table_append(tbl, pa.table([column], names=[new_header]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)

    def encode_category_one_hot(self, canonical: pa.Table, headers: [str, list]=None, prefix=None, data_type: pa.Table=None,
                                prefix_sep: str=None, dummy_na: bool = False, drop_first: bool = False, seed: int=None,
                                save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                                replace_intent: bool=None, remove_duplicates: bool=None) -> pd.DataFrame:
        """ encodes categorical data types, One hot encoding, consists in encoding each categorical variable with
        different boolean variables (also called dummy variables) which take values 0 or 1, indicating if a category
        is present in an observation.

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply encoding too
        :param prefix: str, list of str, or dict of str, String to append DataFrame intent levels, with equal length.
        :param prefix_sep: str separator, default '_'
        :param dummy_na: Add a column to indicate null values, if False nullss are ignored.
        :param drop_first:  Whether to get k-1 dummies out of k categorical levels by removing the first level.
        :param data_type: Data type for new columns. Only a single dtype is allowed.
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _ = self._seed() if seed is None else seed
        prefix_sep = prefix_sep if isinstance(prefix_sep, str) else "_"
        dummy_na = dummy_na if isinstance(dummy_na, bool) else False
        drop_first = drop_first if isinstance(drop_first, bool) else False
        d_type = data_type if data_type else pa.int64()
        dummies = pd.get_dummies(canonical.to_pandas(), columns=headers, prefix=prefix, prefix_sep=prefix_sep,
                              dummy_na=dummy_na, drop_first=drop_first, dtype=data_type)
        return pa.Table.from_pandas(self, dummies)

    def scale_normalize(self, canonical: pa.Table, headers: [str, list]=None, scalar: [tuple, str]=None,
                        prefix: str=None, precision: int=None, seed: int=None, save_intent: bool=None,
                        intent_level: [int, str]=None, intent_order: int=None, replace_intent: bool=None,
                        remove_duplicates: bool=None):
        """ Normalization of continuous data using either Min-Max Scaling or Robust Scaling, dependent on the
        scalar passed.

        Min-Max Scaling: scales the data such that it falls within a specified range, typically (0,1) as default if
        no value is passed, or (min, max) tuple. This method is suitable when your data should be uniformly
        distributed across the specified range.

        Robust Scaling: Robust scaling is similar to min-max scaling but is less sensitive to outliers. It uses
        the interquartile range (0.25, 0.75) to scale the data. This is used if the scalar equals 'robust'.
        Robust scaling is particularly useful when your dataset contains outliers or when the underlying data
        distribution is not necessarily Gaussian

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply scaling too
        :param scalar:(optional) a tuple scalar representing min and max values or 'robust' for interquartile scaling
        :param prefix: (optional) a str prefix for generated headers
        :param precision: (optional) how many decimal places. default to 3
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _seed = seed if isinstance(seed, int) else self._seed()
        scalar = scalar if isinstance(scalar, (tuple, str)) else (0, 1)
        tbl = None
        for n in headers:
            c = canonical.column(n).combine_chunks()
            if not (pa.types.is_floating(c.type) or pa.types.is_integer(c.type)):
                continue
            precision = precision if isinstance(precision, int) else Commons.column_precision(c)+2
            s_values = c.to_pandas()
            null_idx = s_values[s_values.isna()].index
            s_values = s_values.fillna(0)
            if isinstance(scalar, str) and scalar == 'robust':
                if s_values.max() == s_values.min():
                    s_values = pd.Series([0.5] * canonical.num_rows)
                else:
                    s_values = pd.Series(Commons.list_normalize_robust(s_values.to_list(), precision))
            elif s_values.max() == s_values.min():
                s_values = pd.Series([np.mean([scalar[0], scalar[1]])] * canonical.num_rows)
            else:
                if scalar[0] >= scalar[1] or len(scalar) != 2:
                    scalar = (0,1)
                s_values = pd.Series(Commons.list_normalize(s_values.to_list(), scalar[0], scalar[1]))
            s_values = s_values.round(precision)
            if null_idx.size > 0:
                s_values.iloc[null_idx] = np.nan
            new_header = f"{prefix}{n}"
            tbl = Commons.table_append(tbl, pa.table([s_values], names=[n]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)

    def scale_standardize(self, canonical: pa.Table, headers: [str, list]=None, prefix: str=None, precision: int=None,
                          seed: int=None, save_intent: bool=None, intent_level: [int, str]=None, intent_order: int=None,
                          replace_intent: bool=None, remove_duplicates: bool=None):
        """ Z-Score Standardization (Standard Scaling): This method transforms the data to have a mean of 0
        and a standard deviation of 1. It's particularly useful when your data follows a Gaussian (normal)
        distribution. This transformation makes it easier to compare and work with features that may have
        different scales and ensures that they contribute equally to model training.

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply scaling too
        :param prefix: (optional) a str prefix for generated headers
        :param precision: (optional) how many decimal places. default to 3
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _seed = seed if isinstance(seed, int) else self._seed()
        tbl = None
        for n in headers:
            c = canonical.column(n).combine_chunks()
            if not (pa.types.is_floating(c.type) or pa.types.is_integer(c.type)):
                continue
            precision = precision if isinstance(precision, int) else Commons.column_precision(c)+2
            s_values = c.to_pandas()
            null_idx = s_values[s_values.isna()].index
            s_values = s_values.fillna(0)
            s_values = pd.Series(Commons.list_standardize(s_values.to_list()))
            s_values = s_values.round(precision)
            if null_idx.size > 0:
                s_values.iloc[null_idx] = np.nan
            new_header = f"{prefix}{n}"
            tbl = Commons.table_append(tbl, pa.table([s_values], names=[n]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)

    def scale_transform(self, canonical: pa.Table, transform: str, headers: [str, list]=None, prefix: str=None,
                        precision: int=None, seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                        intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None):
        """ Log, sqrt (square root), cbrt (cube root), Box-Cox, and Yeo-Johnson transformations. These are techniques
        used to modify the distribution or scale of continuous data to make the data conform more closely to a
        normal distribution or to stabilize the variance.

        Log Transformation (log): The log transformation involves taking the natural logarithm of each data point.
        It is particularly useful when dealing with data that follows an exponential distribution or has a
        right-skewed distribution. The log transformation can help make the data more symmetric and stabilize
        the variance.

        Square Root Transformation (sqrt): The square root transformation involves taking the square root of
        each data point. It is often used when dealing with count data or data with a right-skewed distribution.
        Like the log transformation, the square root transformation can make the data more symmetric and stabilize
        the variance.

        Cube Root Transformation (cbrt): The cube root transformation involves taking the cube root of each
        data point. It is another option for stabilizing variance and making data less skewed, especially when
        dealing with positive data with right-skewed distributions.

        Box-Cox Transformation: The Box-Cox transformation is a family of power transformations that includes
        both the log and square root transformations as special cases. Can only work with positive values

        Yeo-Johnson Transformation: The Yeo-Johnson transformation is an extension of the Box-Cox transformation
        that allows for the transformation of data with both positive and negative values.

        These transformations are often applied to address issues like non-normality, heteroscedasticity (unequal variance),
        and skewed distributions in the data.

        :param canonical: pyarrow Table
        :param headers: the header(s) to apply scaling to
        :param transform: transform function, 'log', 'sqrt', 'cbrt', 'boxcox' or 'yeojohnson'
        :param prefix: (optional) a str prefix for generated headers
        :param precision: (optional) how many decimal places. default to 3
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _seed = seed if isinstance(seed, int) else self._seed()
        tbl = None
        for n in headers:
            c = canonical.column(n).combine_chunks()
            if not (pa.types.is_floating(c.type) or pa.types.is_integer(c.type)):
                continue
            precision = precision if isinstance(precision, int) else Commons.column_precision(c)+2
            s_values = c.to_pandas()
            null_idx = s_values[s_values.isna()].index
            s_values = s_values.fillna(0)
            if transform == 'log':
                s_values = np.log(s_values)
            elif transform == 'sqrt':
                s_values = np.sqrt(s_values)
            elif transform == 'cbrt':
                s_values = np.cbrt(s_values)
            elif transform == 'boxcox' or transform.startswith('box'):
                bc, _ = stats.boxcox(s_values.to_numpy())
                s_values = pd.Series(bc)
            elif transform == 'yeojohnson' or transform.startswith("yeo"):
                yj, _ = stats.yeojohnson(s_values.to_numpy())
                s_values = pd.Series(yj)
            else:
                raise ValueError(f"The transformer {transform} is not recognized. See contacts notes for reference")
            s_values = s_values.round(precision)
            if null_idx.size > 0:
                s_values.iloc[null_idx] = np.nan
            new_header = f"{prefix}{n}"
            tbl = Commons.table_append(tbl, pa.table([s_values], names=[n]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)

    def scale_activation(self, canonical: pa.Table, activation: str, headers: [str, list]=None, prefix: str=None,
                         precision: int=None, seed: int=None, save_intent: bool=None, intent_level: [int, str]=None,
                         intent_order: int=None, replace_intent: bool=None, remove_duplicates: bool=None):
        """ An activation function determines the output of a neuron or a node in a neural network or binary
        classification problems. Tanh (Hyperbolic Tangent), Sigmoid, and ReLU (Rectified Linear Unit) are three
        commonly used activation functions. Only applied to numeric values

        Sigmoid Function: Defined as f(x) = 1 / (1 + e^(-x)), the sigmoid function maps its input to a range
        between 0 and 1, which can be interpreted as probabilities. It's often used in the output layer for
        binary classification tasks.

        Hyperbolic Tangent (tanh) Function: Defined as f(x) = (e^(x) - e^(-x)) / (e^(x) + e^(-x)), the tanh
        function maps its input to a range between -1 and 1. It is zero-centered, which can be advantageous
        in some cases.

        Rectified Linear Unit (ReLU): Defined as f(x) = max(0, x), ReLU is a piecewise linear function that
        outputs the input for positive values and zero for negative values. It's computationally efficient
        and has become a popular choice in many deep learning architectures.

        :param canonical: a pyarrow table
        :param headers: the header(s) to apply scaling too
        :param activation: The activation function, 'tanh', 'sigmoid' or 'ReLu'
        :param prefix: (optional) a str prefix for generated headers
        :param precision: (optional) how many decimal places. default to 3
        :param seed: seed: (optional) a seed value for the random function: default to None
        :param save_intent: (optional) if the intent contract should be saved to the property manager
        :param intent_level: (optional) the intent level that groups intent to create a column
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
        self._set_intend_signature(self._intent_builder(method=inspect.currentframe().f_code.co_name, params=locals()),
                                   intent_level=intent_level, intent_order=intent_order, replace_intent=replace_intent,
                                   remove_duplicates=remove_duplicates, save_intent=save_intent)
        # intend code block on the canonical
        canonical = self._get_canonical(canonical)
        headers = Commons.list_formatter(headers) if isinstance(headers, (str, list)) else canonical.column_names
        _seed = seed if isinstance(seed, int) else self._seed()
        tbl = None
        for n in headers:
            c = canonical.column(n).combine_chunks()
            if not (pa.types.is_floating(c.type) or pa.types.is_integer(c.type)):
                continue
            precision = precision if isinstance(precision, int) else Commons.column_precision(c)+2
            s_values = c.to_pandas()
            null_idx = s_values[s_values.isna()].index
            s_values = s_values.fillna(0)
            if activation.startswith('sigmoid'):
                s_values = np.round(1 / (1 + np.exp(-s_values)), precision)
            elif activation.startswith('tanh'):
                s_values = np.round((np.exp(s_values)-np.exp(-s_values))/(np.exp(s_values)+np.exp(-s_values)), precision)
            elif activation.startswith('relu'):
                s_values = np.round(s_values * (s_values > 0), precision)
            else:
                raise ValueError(f"The activation function '{activation}' is not supported. Current available options "
                                 f"are 'sigmoid', 'tanh' and 'ReLu'")
            s_values = pd.Series(s_values)
            if null_idx.size > 0:
                s_values.iloc[null_idx] = np.nan
            new_header = f"{prefix}{n}"
            tbl = Commons.table_append(tbl, pa.table([s_values], names=[n]))
        if not tbl:
            return canonical
        return Commons.table_append(canonical, tbl)
