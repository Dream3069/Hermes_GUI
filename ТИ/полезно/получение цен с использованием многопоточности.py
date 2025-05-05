from datetime import datetime, timedelta, timezone
from pandas import DataFrame
from tensorflow.python.ops.numpy_ops.np_math_ops import argsort
from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle, InstrumentIdType
import creds
import pandas as pd
pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

# функция для получения списка всех акций на тинькоффе
def all_stocks():
    try:
        with Client(creds.TOKEN) as client:
            lst = []
            lst1 = client.instruments.shares()
            stocks_lst = lst1.instruments
            for i in range(len(stocks_lst)):
                # Получение списка акций
                stocks = stocks_lst[i]
                lst.append([stocks.ticker, stocks.figi])
            return lst

    except RequestError as e:
        print(str(e))

class get_table():
    def get_price(self, figi, days=0):
        try:
            with Client(creds.TOKEN) as client:
                r = client.market_data.get_candles(
                    figi=figi,
                    from_=datetime.now(timezone.utc) - timedelta(days=days + 1),
                    to=datetime.now(timezone.utc) - timedelta(days=days),
                    interval=CandleInterval.CANDLE_INTERVAL_15_MIN  # см. utils.get_all_candles
                )
                # print(r)
                df = get_table().create_df(r.candles)
                # print(df[['time', 'close']].tail(50))
                return df

        except RequestError as e:
            print(str(e))

    def create_df(self, candles: [HistoricCandle]):
        df = DataFrame([{
            # +3 часа
            'Time': c.time + timedelta(hours=3),
            'Volume': c.volume,
            'Open': get_table().cast_money(c.open),
            'Close': get_table().cast_money(c.close),
            'High': get_table().cast_money(c.high),
            'Low': get_table().cast_money(c.low),
        } for c in candles])
        return df

    def cast_money(self, v):
        return v.units + v.nano / 1e9

    def create_table(self, ticker, figi):
        df = pd.DataFrame({})
        data = 1
        df = pd.concat([df, get_table().get_price(figi, data)], axis=0, ignore_index=True)
        print(f'записано {data} дней, акция: {ticker}')
        while not (df.empty) and data < 5:
            data += 1
            df = pd.concat([df, get_table().get_price(figi, data)], axis=0, ignore_index=True)
            print(f'записано {data} дней, акция: {ticker}')
            # df += get_info().get_price(figi, data)
            # print(len(get_info().get_price(figi, data)))

        # удаление первого стобца для иишки
        # df.drop(df.columns[[0]], axis=1, inplace=True)
        # сохранение таблицы
        csv_file_path=f'{ticker}_{data}d__{datetime.now().date()}.csv'
        df.to_csv(csv_file_path, index=False)
        print(f'CSV file "{csv_file_path}" был успешно создан')
        # df.drop(df.columns[[0]], axis=1, inplace=True)
        return df

def creat_mylti(index):
    # получение таблицы с ценой акции
    # get_table().create_table(ticker, figi, days)
    return get_table().create_table(stocks_lst[index][0], stocks_lst[index][1])

# список всех акций
stocks_lst = all_stocks()
print(stocks_lst)

# создание файлов с использованием многопоточности
import threading
count_stocks = 5 #len(stocks_lst)
for i in range(0, count_stocks, 4):
    thread1 = threading.Thread(target=creat_mylti, args=(i,))
    thread2 = threading.Thread(target=creat_mylti, args=(i+1,))
    thread3 = threading.Thread(target=creat_mylti, args=(i+2,))
    thread4 = threading.Thread(target=creat_mylti, args=(i+3,))

    thread1.start()
    thread2.start()
    thread3.start()
    thread4.start()

    thread1.join()
    thread2.join()
    thread3.join()
    thread4.join()

"""
time_when = datetime.now(timezone.utc)
for i in range(0,4,2):
    thread1 = threading.Thread(target=creat_mylti, args=(i,))
    thread2 = threading.Thread(target=creat_mylti, args=(i+1,))
    thread1.start()
    thread2.start()
    thread1.join()
    thread2.join()
time_now = datetime.now(timezone.utc)
print(time_now - time_when, "затраченно времени")
"""