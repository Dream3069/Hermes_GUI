import pandas_ta as ta
import pandas as pd

#import pylab
#from matplotlib import pyplot as plt
#import yfinance as yf

#df = yf.Ticker('BTC-USD').history(period='1y')[['Close', 'Open', 'High', 'Volume', 'Low']]
def MACD(df):
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
        df["signal_buy"] = df["signal_buy"] + buy
        df["signal_sell"] = df["signal_sell"] + sell
    except KeyError:
        df["signal_buy"] = buy
        df["signal_sell"] = sell
    return df

"""df = MACD(df)
print(df)
#df['sell'] = np.where((80 <= df.K) & (df.K <= df.D) & (df.D >= 80), 1, 0)
pylab.subplot(2, 1, 2)
pylab.plot(df["Close"])
pylab.subplot(2, 1, 1)
pylab.plot(df["signal_buy"])
pylab.plot(df["signal_sell"])
plt.show()"""