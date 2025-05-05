from datetime import datetime, timedelta, timezone
from pandas import DataFrame
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

    def create_table(self, ticker, figi, days):
        proch = 0
        df = pd.DataFrame({})
        for data in range(days, 1, -1):
            df = pd.concat([df, get_table().get_price(figi, data)], axis=0, ignore_index=True)
            # df += get_info().get_price(figi, data)
            # print(len(get_info().get_price(figi, data)))
            proch += 1
            print(f'готово на {proch}/{days}')

        # удаление первого стобца для иишки
        # df.drop(df.columns[[0]], axis=1, inplace=True)
        # сохранение таблицы
        csv_file_path=f'{ticker}_{days}d_15m_28.09.2024.csv'
        df.to_csv(csv_file_path, index=False)
        print(f'CSV file "{csv_file_path}" был успешно создан')
        # df.drop(df.columns[[0]], axis=1, inplace=True)
        return df


print(all_stocks())
# stocks = [stocks.ticker, stocks.figi]
test_srocks = all_stocks()[0]
# create_table(ticker, figi, days) , create_table(ticker=test_srocks[0], figi=test_srocks[1], days=10)
get_table().create_table(test_srocks[0], test_srocks[1], 10)


"""import threading

def print_numbers():
    for i in range(10):
        print(i)

def print_letters():
    for letter in 'abcdefghij':
        print(letter)

# Создаём потоки
thread1 = threading.Thread(target=print_numbers)
thread2 = threading.Thread(target=print_letters)

# Запускаем потоки
thread1.start()
thread2.start()

# Ждём завершения потоков
thread1.join()
thread2.join()

"""