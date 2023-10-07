import time
import numpy as np
import pandas as pd
from ds_core.handlers.abstract_handlers import ConnectorContract

__author__ = 'Darryl Oatridge'


class CommonsIntentModel(object):

    @classmethod
    def __dir__(cls):
        """returns the list of available methods associated with the parameterized intent"""
        rtn_list = []
        for m in dir(cls):
            if not m.startswith('_'):
                rtn_list.append(m)
        return rtn_list

    """
        PRIVATE METHODS SECTION
    """

    @staticmethod
    def _seed(seed: int=None, increment: bool=False):
        if not isinstance(seed, int):
            return int(time.time() * np.random.default_rng().random())
        if increment:
            seed += 1
            if seed > 2 ** 31:
                seed = int(time.time() * np.random.default_rng(seed=seed-1).random())
        return seed

    def _set_quantity(self, selection, quantity, seed=None):
        """Returns the quantity percent of good values in selection with the rest fill"""
        quantity = self._quantity(quantity)
        if quantity == 1:
            return selection
        if quantity == 0:
            return [np.nan] * len(selection)
        seed = self._seed(seed=seed)
        quantity = 1 - quantity
        generator = np.random.default_rng(seed)
        length = len(selection)
        size = int(length * quantity)
        nulls_idx = generator.choice(length, size=size, replace=False)
        result = pd.Series(selection)
        result.iloc[nulls_idx] = np.nan
        return result.to_list()

    @staticmethod
    def _quantity(quantity: [float, int]) -> float:
        """normalises quantity to a percentate float between 0 and 1.0"""
        if not isinstance(quantity, (int, float)) or not 0 <= quantity <= 100:
            return 1.0
        if quantity > 1:
            return round(quantity / 100, 2)
        return float(quantity)


    @staticmethod
    def _extract_value(value: [str, int, float]):
        if isinstance(value, str):
            if value.startswith('${') and value.endswith('}'):
                value = ConnectorContract.parse_environ(value)
                if value.isnumeric():
                    return int(value)
                elif value.replace('.', '', 1).isnumeric():
                    return float(value)
                else:
                    return str(value)
            else:
                return str(value)
        return value

    """
        UTILITY METHODS SECTION
    """

    @staticmethod
    def _freq_dist_size(relative_freq: list, size: int, dist_length: int=None, dist_on: str=None, seed: int=None):
        """ utility method taking a list of relative frequencies and based on size returns the size distribution
        of element based on the frequency. The distribution is based upon binomial distributions.

        :param relative_freq: a list of int or float values representing a relative distribution frequency
        :param size: the size of the values to be distributed
        :param dist_length: (optional) the expected length of the element's in relative_freq
        :param dist_on: (optional) if element length differs. distribute on 'left', 'right' or 'center'. Default 'right'
        :param seed: (optional) a seed value for the random function: default to None
        :return: an integer list of the distribution that sum to the size
        """
        if not isinstance(relative_freq, list) or not all(isinstance(x, (int, float)) for x in relative_freq):
            raise ValueError("The weighted pattern must be an list of numbers")
        dist_length = dist_length if isinstance(dist_length, int) else len(relative_freq)
        dist_on = dist_on if dist_on in ['right', 'left'] else 'both'
        seed = seed if isinstance(seed, int) else int(time.time() * np.random.random())
        # sort the width
        if len(relative_freq) > dist_length:
            a = np.array(relative_freq)
            trim = dist_length - a.size
            if dist_on.startswith('right'):
                relative_freq = a[:trim]
            elif dist_on.startswith('left'):
                relative_freq = a[abs(trim):]
            else:
                l_size = int(trim/2)
                r_size = a.size + l_size - dist_length
                relative_freq = a[r_size:l_size].tolist()
        if len(relative_freq) < dist_length:
            a = np.array(relative_freq)
            rvalue = a[-1:]
            lvalue = a[:1]
            if dist_on.startswith('left'):
                r_dist = []
                l_dist = np.tile(lvalue, dist_length - a.size)
            elif dist_on.startswith('right'):
                r_dist = np.tile(rvalue, dist_length - a.size)
                l_dist = []
            else:
                l_size = int((dist_length - a.size) / 2)
                r_dist = np.tile(rvalue, l_size)
                l_dist = np.tile(lvalue, dist_length - l_size - a.size)
            relative_freq = np.hstack([l_dist, a, r_dist]).tolist()
        # turn it to percentage
        if sum(relative_freq) != 1:
            relative_freq = np.round(relative_freq / np.sum(relative_freq), 5)
        generator = np.random.default_rng(seed=seed)
        result = list(generator.binomial(n=size, p=relative_freq, size=len(relative_freq)))
        diff = size - sum(result)
        adjust = [0] * len(relative_freq)
        # There is a possibility the required size is not fulfilled, therefore add or remove elements based on freq
        if diff != 0:
            unit = diff / sum(relative_freq)
            for idx in range(len(relative_freq)):
                adjust[idx] = int(round(relative_freq[idx] * unit, 0))
        result = [a + b for (a, b) in zip(result, adjust)]
        # rounding can still make us out by 1
        if sum(result) != size:
            gap = sum(result) - size
            result[result.index(max(result))] -= gap
        return result[:size]
