import pandas_ta as ta
import yfinance as yf
import numpy as np
class analiz():
    def MACD(self, df):
        # Calculate MACD values using the pandas_ta library
        df.ta.macd(close='Close', fast=12, slow=26, signal=9, append=True)
        buy = []
        sell = []
        for x in range(len(df)):
            if df['MACDs_12_26_9'].iloc[x] >= df["MACDh_12_26_9"].iloc[x] and df["MACDh_12_26_9"].iloc[x-1] < df['MACDs_12_26_9'].iloc[x-1]:
                buy.append(0)
                sell.append(1)
            elif df['MACDs_12_26_9'].iloc[x] <= df["MACDh_12_26_9"].iloc[x] and df["MACDh_12_26_9"].iloc[x-1] > df['MACDs_12_26_9'].iloc[x-1]:
                buy.append(1)
                sell.append(0)
            else:
                buy.append(0)
                sell.append(0)
        try:
            df["signal_buy_MACD"] = df["signal_buy_MACD"] + buy
            df["signal_sell_MACD"] = df["signal_sell_MACD"] + sell
        except KeyError:
            df["signal_buy_MACD"] = buy
            df["signal_sell_MACD"] = sell
        return df

    def RSI(self, df):
        df['RSI'] = ta.rsi(df['Close'], 2)
        i = np.where(df.RSI < 30, 1, 0)
        t = np.where(df.RSI > 80, 1, 0)
        try:
            df["signal_buy_RSI"] = df["signal_buy_RSI"] + i
            df["signal_sell_RSI"] = df["signal_sell_RSI"] + t
        except KeyError:
            df["signal_buy_RSI"] = i
            df["signal_sell_RSI"] = t
        return df

    def counting_strategy(self):
        df = yf.Ticker('BTC-USD').history(period='1y')[['Close', 'Open', 'High', 'Volume', 'Low']]
        df = analiz().RSI(df)
        df = analiz().MACD(df)
        return df.to_string()


print(analiz().counting_strategy())
