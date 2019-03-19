""" Aroon Indicator
"""

import talib
import pandas
import math

from analyzers.utils import IndicatorUtils
from analyzers.indicators.line_utils import LineUtils


class Aroon(IndicatorUtils):

    def check_intersect(self, aroondown, aroonup, periods_back):

        old_down = (aroondown.index[-periods_back].timestamp(), aroondown[-periods_back])
        current_down = (aroondown.index[-1].timestamp(), aroondown[-1])

        old_up = (aroonup.index[-periods_back].timestamp(), aroonup[-periods_back])
        current_up = (aroonup.index[-1].timestamp(), aroonup[-1])

        line = LineUtils()

        return line.doIntersect(old_down, current_down, old_up, current_up)        


    def is_hot(self, aroondown, aroonup):
        
        periods_back = 6

        if self.check_intersect(aroondown, aroonup, periods_back) :
            self.logger.info('Found cross 6 periods back')
            return 1 if aroonup[-1] > aroondown[-1] else -1

        periods_back = 8

        if self.check_intersect(aroondown, aroonup, periods_back) :
            self.logger.info('Found cross 8 periods back')
            return 1 if aroonup[-1] > aroondown[-1] else -1

        #No crossing lines        
        return 0

    def analyze(self, historical_data, period_count=14, signal=['close'], hot_thresh=None, cold_thresh=None):
        """Performs an analysis about the increase in volumen on the historical data

        Args:
            historical_data (list): A matrix of historical OHCLV data.
            signal (list, optional): Defaults to close. Unused in this indicator

        Returns:
            pandas.DataFrame: A dataframe containing the indicator and hot/cold values.
        """

        dataframe = self.convert_to_dataframe(historical_data)

        aroondown, aroonup = talib.AROON(dataframe['high'], dataframe['low'], timeperiod=period_count)

        aroon = pandas.concat([dataframe, aroondown, aroonup], axis=1)
        aroon.rename(columns={0: 'aroondown', 1: 'aroonup'}, inplace=True)        

        aroon['is_hot']  = False
        aroon['is_cold'] = False

        is_hot = self.is_hot(aroondown, aroonup)

        aroon['is_hot'].iloc[-1] = is_hot == 1
        aroon['is_cold'].iloc[-1] = is_hot == -1

        return aroon