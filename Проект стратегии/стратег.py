import pandas_ta as ta
import pandas as pd
import matplotlib.pyplot as plt
def BB_SO_RSI(df):
    # length от 13 до 24 std от 2 до 5 настройка для BB
    df[['BB_lower', 'BB_mid', 'BB_upper']] = ta.bbands(df.Close, length=20, std=2).iloc[:, :3]
    # k = 14 d = 3
    df[["K", "D"]] = ta.stoch(high=df.High, low=df.Low, close=df.Close, k=14, d=2, smooth_k=2, append=True)
    df['RSI'] = ta.rsi(df['Close'], 2)
    df['SMA_30'] = ta.sma(close=df.Close, length=30)
    df[['MACD_12_26_9_blue', 'MACDh_12_26_9_red', 'MACDs_12_26_9_orange']] = df.ta.macd(close='close', fast=12, slow=26, signal=9, append=True)
    # не оч df[['AROOND_14', 'AROONU_14', 'AROONOSC_14']] = ta.aroon(df['High'], df['Low'], length=14)
    # не оч df['MFI_14'] = ta.mfi(df['High'], df['Low'], df['Close'], df['Volume'])
    df[['ADX_14', '+DMP_14', '-DMN_14']] = ta.adx(df['High'], df['Low'], df['Close'])
    print(df)
    # df["signal_buy_SO_RSI"] = np.where((df.K > df.D) & (df.K < 20) & (df.D < 20) & (df.RSI < 30), 1, 0)
    # df["signal_sell_SO_RSI"] = np.where((df.K < df.D) & (df.K > 80) & (df.D > 80) & (df.RSI > 70), 1, 0)
    action = "buy"
    buy = []
    sell = []
    profit = []
    broker = 0.003 # 0.3% = 0.003 комиссия тинькоффа
    stop_loss = 0
    for x in range(len(df)):
        # восходящий покупка buy
        if (df['Low'].iloc[x] + 0.5 < df['BB_lower'].iloc[x]) and (df['RSI'].iloc[x] < 30) and (df['K'].iloc[x] < 20) and (df['D'].iloc[x] < 20)\
                and (df['Close'].iloc[x] < df['SMA_30'].iloc[x])\
                and (df['MACDh_12_26_9_red'].iloc[x-1] > df['MACDh_12_26_9_red'].iloc[x])\
                and (df['-DMN_14'].iloc[x] > df['+DMP_14'].iloc[x])\
                and action == "buy":
            buy.append(1)
            buy_price_1 = df['Close'].iloc[x]
            sell.append(0)
            lst = ['buy', df['Close'].iloc[x], df['Time'].iloc[x]]
            action = "sell"
            profit.append(lst)
            stop_loss = take_stop_profit(df, x)[0]
            print(df['SMA_30'].iloc[x], df['Time'].iloc[x], 'buy')
        # нисходящий продажа sell
        elif ((df['High'].iloc[x] + 0.5 > df['BB_upper'].iloc[x]) and (df['RSI'].iloc[x] > 70) and (df['K'].iloc[x] > 80) and (df['D'].iloc[x] > 80)\
                and (df['Close'].iloc[x] > df['SMA_30'].iloc[x])\
                and (df['MACDh_12_26_9_red'].iloc[x-1] < df['MACDh_12_26_9_red'].iloc[x]) \
                and (df['-DMN_14'].iloc[x] < df['+DMP_14'].iloc[x]) \
                and action == "sell")\
                or (df['Close'].iloc[x] <= stop_loss and action == "sell"):
            buy.append(0)
            sell.append(1)
            lst = ['sell', df['Close'].iloc[x], df['Time'].iloc[x]]
            action = "buy"
            profit.append(lst)
            print(df['SMA_30'].iloc[x], df['Time'].iloc[x], 'sell')
        # бай бай
        else:
            buy.append(0)
            sell.append(0)
    print(profit)

    df["signal_buy_BB"] = buy
    df["signal_sell_BB"] = sell
    return df
# hdfkghdkhgkdhfgkdkfgh

def take_stop_profit(df, index=0, action='long'):
    data_close = [float(i) * 0.54 for i in df['Low'][index-20:index+1]]
    if action == 'long':
        # значение для stop_loss
        stop_loss_for_bull = min(data_close[-20:-1])
        take_profit_for_bull = max(data_close[-20:-1])
        return stop_loss_for_bull, take_profit_for_bull
    elif action == 'short':
        # значение для stop_loss
        stop_loss_for_bear = max(data_close[-21:-1])
        take_profit_for_bear = min(data_close[-21:-1])
        return stop_loss_for_bear, take_profit_for_bear


df = pd.read_csv('SBER_365d_15m_28.09.2024.csv')
df = BB_SO_RSI(df)

# Сброс ограничений на число столбцов
pd.set_option('display.max_columns', None)
# Сброс ограничений на количество символов в записи
pd.set_option('display.max_colwidth', None)
print(df)

buy_price = 0
sell_price = 0
k_b = 0
k_s = 0
action = "buy"
g = []
f = []
komisia = 1.003
buy_price_last = 0
k_p = 0
for i in range(2, len(df)):
    if df['signal_buy_BB'].iloc[i] == 1 and action == "buy":
        buy_price += df['Close'].iloc[i]
        g.append(df['Close'].iloc[i])
        action = "sell"
        k_b += 1
        buy_price_last = df['Close'].iloc[i]
    elif df['signal_sell_BB'].iloc[i] == 1 and action == "sell":
        sell_price += df['Close'].iloc[i]
        f.append(df['Close'].iloc[i])
        action = "buy"
        k_s += 1
        if df['Close'].iloc[i] - buy_price_last > 0:
            k_p += 1
        else:
            print(df['Close'].iloc[i] - buy_price_last, 'минус', df['Time'].iloc[i])

print(f'прибыль {(sell_price - buy_price) * komisia}')
print(f'сумма продаж {sell_price} покупки {buy_price}')
print(f'количество продаж {k_s} и покупок {k_b}, кол-во удачных сделок {k_p}')
print(f'последняя цена покупки: {buy_price_last}')

plt.plot(df["Close"])

plt.plot(df["Close"] * komisia)

plt.plot(df[df.signal_buy_BB==1]['Close'], '^g')
plt.plot(df[df.signal_sell_BB==1]['Close'], 'vr')

plt.show()
# ['buy', 326.88, '2024-07-01 18:00:00+00:00'], ['sell', 327.83, '2024-07-02 11:00:00+00:00'],  +
# ['buy', 328.78, '2024-07-03 18:45:00+00:00'], ['sell', 324.57, '2024-07-05 23:00:00+00:00'],  -
# ['buy', 325.07, '2024-07-08 11:15:00+00:00'], ['sell', 316.68, '2024-07-10 23:45:00+00:00'],  -
# ['buy', 289.53, '2024-07-11 10:30:00+00:00'], ['sell', 291.49, '2024-07-11 14:15:00+00:00'],  +
# ['buy', 292.11, '2024-07-12 11:15:00+00:00'], ['sell', 285.35, '2024-07-16 22:30:00+00:00'],  -
# ['buy', 295.47, '2024-07-24 22:15:00+00:00'], ['sell', 296.35, '2024-07-25 13:45:00+00:00'],  +
#
# ['buy', 294.87, '2024-07-26 15:00:00+00:00']

# [['buy', 326.88, '2024-07-01 18:00:00+00:00'], ['sell', 327.83, '2024-07-02 11:00:00+00:00'],
# ['buy', 328.78, '2024-07-03 18:45:00+00:00'], ['sell', 324.57, '2024-07-05 23:00:00+00:00'],
# ['buy', 325.07, '2024-07-08 11:15:00+00:00'], ['sell', 316.68, '2024-07-10 23:45:00+00:00'],
# ['buy', 289.53, '2024-07-11 10:30:00+00:00'], ['sell', 291.49, '2024-07-11 14:15:00+00:00'],
# ['buy', 292.11, '2024-07-12 11:15:00+00:00'], ['sell', 285.35, '2024-07-16 22:30:00+00:00'],
# ['buy', 295.47, '2024-07-24 22:15:00+00:00'], ['sell', 296.35, '2024-07-25 13:45:00+00:00'],
# ['buy', 294.87, '2024-07-26 15:00:00+00:00']]
# -310.7699999999995 293.4

# прибыль -310.44000000000005 -17
# сумма продаж 1842.27 покупки 2152.71
# количество продаж 6 и покупок 7, кол-во удачных сделок 3
# 294.87


#профит -9 кол-во 31 продажа покупка удач 9

#профит -7 кол-во 32 11 удач
