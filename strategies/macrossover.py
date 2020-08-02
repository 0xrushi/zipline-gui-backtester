import numpy as np
import pandas as pd
import zipline
from yahoofinancials import YahooFinancials
import warnings
import pandas_datareader as pdr
from zipline.api import order, record, symbol, set_benchmark
import zipline
import pytz
import zipline
from datetime import datetime
import pytz
import json


def TradingAlgo(panel, symb):
    def initialize(context):
        context.symbol = symbol(symb)

    def handle_data(context, data):
        todays_pr = data.current(context.symbol, 'price')
        diff = context.portfolio.cash - todays_pr

        hist = data.history(context.symbol, 'price', 35, '1d')
        sma_35 = hist.mean()
        sma_5 = hist[-5:].mean()
        # print(hist)
        record(sma_35=sma_35)
        record(sma_5=sma_5)
        record(close=data.current(context.symbol, 'close'))
        record(open=data.current(context.symbol, 'open'))
        record(high=data.current(context.symbol, 'high'))
        record(low=data.current(context.symbol, 'low'))

        if diff > 0:
            # Trading logic
            if sma_5 > sma_35:
                # order_target orders as many shares as needed to
                # achieve the desired number of shares.
                order(symbol("AAPL"), 2)
            elif sma_5 < sma_35:
                order(symbol("AAPL"), -2)

    perf = zipline.run_algorithm(start=datetime(2017, 3, 27, 0, 0, 0, 0, pytz.utc),
                                 end=datetime(2019, 6, 28, 0,
                                              0, 0, 0, pytz.utc),
                                 initialize=initialize,
                                 capital_base=100,
                                 handle_data=handle_data,
                                 data=panel)
    return perf
