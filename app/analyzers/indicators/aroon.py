""" Aroon Indicator
"""

import talib
import pandas
import math

from analyzers.utils import IndicatorUtils


class Aroon(IndicatorUtils):

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

        old_down, old_up = aroon.iloc[-2]['aroondown'] , aroon.iloc[-2]['aroonup']
        current_down, current_up = aroon.iloc[-1]['aroondown'] , aroon.iloc[-1]['aroonup']

        aroon['is_hot']  = False
        aroon['is_cold'] = False

        aroon['is_hot'].iloc[-1] = old_down > old_up and current_down < current_up
        aroon['is_cold'].iloc[-1] = old_down < old_up and current_down > current_up

        return aroon