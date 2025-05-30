import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import yfinance as yf
df = yf.Ticker('BTC-USD').history(period='1mo', interval='5m')[['Close', 'Open', 'High', 'Volume', 'Low']]


def bands(df):
    df['sma'] = df['Close'].rolling(window=20).mean()
    df['std'] = df['Close'].rolling(window=20).std()

    df['upper_band'] = df['sma'] + (df['std'] * 2)
    df['lower_band'] = df['sma'] - (df['std'] * 2)

    signal_buy = [0]
    signal_sell = [0]
    for i in range(1, len(df)):
        # buy
        if (df['Close'][i] < df['lower_band'][i]) and (df['Close'][i] < df['sma'][i]) and (df['Close'][i-1] >= df['lower_band'][i-1]):
            signal_buy.append(1)
            signal_sell.append(0)
        # sell
        elif (df['Close'][i] > df['upper_band'][i]) and (df['Close'][i] > df['sma'][i]) and (df['Close'][i-1] <= df['upper_band'][i-1]):
            signal_buy.append(0)
            signal_sell.append(1)
        else:
            signal_buy.append(0)
            signal_sell.append(0)

    df['signal_buy'] = signal_buy
    df['signal_sell'] = signal_sell

    return df



bands(df)
pd.set_option('display.max_columns', None)
print(df)


buy_price = 0
sell_price = 0
buy_price_last = 0

k_b = 0
k_s = 0
action = 'buy'
for i in range(50, len(df)):
    if df['signal_buy'][i] == 1 and action == 'buy':
        buy_price += df['Close'][i]
        action = 'sell'
        k_b += 1
        buy_price_last = df['Close'][i]
    elif df['signal_sell'][i] == 1 and action == 'sell':
        sell_price += df['Close'][i]
        action = 'buy'
        k_s += 1

if k_s == k_b:
    print(sell_price - buy_price)
    print(k_s, k_b)
else:
    print(sell_price - buy_price + buy_price_last)
    print(k_s, k_b)

def paint_bands(df):
    plt.plot(df['Close'])
    plt.plot(df['upper_band'])
    plt.plot(df['lower_band'])
    plt.plot(df['sma'])
    plt.legend(['Close', 'upper_band', 'lower_band', 'sma'])
    plt.show()
# paint_bands(df)