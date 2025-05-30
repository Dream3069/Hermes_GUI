import pandas_ta as ta
import numpy as np
def RSI(df):
    df['RSI'] = ta.rsi(df['Close'], 2)
    i = np.where(df.RSI < 30, 1, 0)
    t = np.where(df.RSI > 80, 1, 0)
    try:
        df["signal_buy"] = df["signal_buy"] + i
        df["signal_sell"] = df["signal_sell"] + t
    except KeyError:
        df["signal_buy"] = i
        df["signal_sell"] = t
    return df

"""print(df['RSI'])
pylab.subplot(2, 1, 2)
pylab.plot(df["Close"])
pylab.subplot(2, 1, 1)
#pylab.plot(df["RSI"])
pylab.plot(df["buy"])
pylab.plot(df["sell"])
plt.show()"""