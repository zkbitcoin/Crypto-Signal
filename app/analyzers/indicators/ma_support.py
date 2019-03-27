
""" 
Bollinger Bands indicator
"""

from talib import abstract
import pandas
import math

from analyzers.utils import IndicatorUtils


class MASupport(IndicatorUtils):

    def analyze(self, historical_data, signal=['close'], hot_thresh=None, cold_thresh=None, exponential = True, ma = 99):
        """Check when close price cross some the MA defined for parameter "ma". Example EMA(99) or MA(100)

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to close. Unused for this indicator
            exponential (boolean): flag to indicate is EMA is used
            ma (integer): periods to use to calculate the MA

        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)

        if exponential == True:
            ma_values = abstract.EMA(dataframe, ma)
        else:
            ma_values = abstract.SMA(dataframe, ma)

        ma_support = pandas.concat([dataframe, ma_values], axis=1)
        ma_support.rename(columns={0: 'ma'}, inplace=True)

        old_close = ma_support.iloc[-2]['close']
        cur_close = ma_support.iloc[-1]['close']
        cur_low   = ma_support.iloc[-1]['low']

        old_ma = ma_support.iloc[-2]['ma']
        cur_ma = ma_support.iloc[-1]['ma']

        ma_support['is_hot']  = False
        ma_support['is_cold'] = False

        ma_support['is_hot'].iloc[-1] = old_ma < old_close and (cur_ma > cur_close or cur_ma > cur_low)

        return ma_support