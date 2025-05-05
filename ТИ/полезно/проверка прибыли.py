import yfinance as yf
import pandas as pd

# Request historic pricing data via finance.yahoo.com API
df = yf.Ticker('AREB').history(period='1d', interval='5m')[['Close', 'Open', 'High', 'Volume', 'Low']]

def macd(df):
    # Get the 26-day EMA of the closing price
    k = df['Close'].ewm(span=12, adjust=False, min_periods=12).mean()
    # Get the 12-day EMA of the closing price
    d = df['Close'].ewm(span=26, adjust=False, min_periods=26).mean()
    # Subtract the 26-day EMA from the 12-Day EMA to get the MACD
    macd = k - d
    # Get the 9-Day EMA of the MACD for the Trigger line
    macd_s = macd.ewm(span=9, adjust=False, min_periods=9).mean()
    # Calculate the difference between the MACD - Trigger for the Convergence/Divergence value
    macd_h = macd - macd_s
    # Add all of our new values for the MACD to the dataframe
    df['macd'] = df.index.map(macd)
    df['macd_h'] = df.index.map(macd_h)
    df['macd_s'] = df.index.map(macd_s)

    # рассчет покупки и продажи
    signal_buy = [0]
    signal_sell = [0]
    for i in range(1, len(df)):
        if (df['macd_h'][i-1] < 0) and (df['macd_h'][i] > 0):
            signal_buy.append(1)
            signal_sell.append(0)
        elif (df['macd_h'][i-1] > 0) and (df['macd_h'][i] < 0):
            signal_buy.append(0)
            signal_sell.append(1)
        else:
            signal_buy.append(0)
            signal_sell.append(0)
    # чистка
    df.drop('macd', axis=1, inplace=True)
    df.drop('macd_h', axis=1, inplace=True)
    df.drop('macd_s', axis=1, inplace=True)



    df['signal_buy'] = signal_buy
    df['signal_sell'] = signal_sell
    return df




macd(df)


# profit
buy_price_last = 0
buy_price = 0
sell_price = 0

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
    print(k_s, k_b-1)


