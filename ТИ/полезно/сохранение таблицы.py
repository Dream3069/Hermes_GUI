"""import csv
with open("classmates.csv", mode="w", encoding='utf-8') as w_file:
    file_writer = csv.writer(w_file, delimiter = ",", lineterminator="\r")
    file_writer.writerow(["Имя", "Класс", "Возраст"])
    file_writer.writerow(["Женя", "3", "10"])
    file_writer.writerow(["Саша", "5", "12"])
    file_writer.writerow(["Маша", "11", "18"])"""

"""# importing csv
import csv

# Data
data = [
    ['Name', 'Age', 'City'],
    ['Aman', 28, 'Pune'],
    ['Poonam', 24, 'Jaipur'],
    ['Bobby', 32, 'Delhi']
]

# File path for the CSV file
csv_file_path = 'example.csv'

# Open the file in write mode
with open(csv_file_path, mode='w', newline='') as file:
    # Create a csv.writer object
    writer = csv.writer(file)
    # Write data to the CSV file
    writer.writerows(data)

# Print a confirmation message
print(f"CSV file '{csv_file_path}' created successfully.")"""

# работа с таблицами
"""
# Step 1 Importing pandas
import pandas as pd
 
# Step 2 Prepare your data
data = {
    'Name': ['Rajat', 'Tarun', 'Bobby'],
    'Age': [30, 25, 35],
    'City': ['New York', 'Delhi', 'Pune']
}
 
# Step 3 Create a DataFrame using DataFrame function
df = pd.DataFrame(data)
 
# Step 4 Specify the file path to save data
csv_file_path = 'data.csv'
 
# Step 5 Write the DataFrame to a CSV file using to_csv() function where file path is passed
df.to_csv(csv_file_path, index=False)
 
print(f'CSV file "{csv_file_path}" has been created successfully.')"""

from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle

import creds
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class get_info():
    def get_price(self, figi, days=0):
        try:
            with Client(creds.TOKEN) as client:
                r = client.market_data.get_candles(
                    figi=figi,
                    from_=datetime.now(timezone.utc) - timedelta(days=days+1),
                    to=datetime.now(timezone.utc) - timedelta(days=days),
                    interval=CandleInterval.CANDLE_INTERVAL_15_MIN  # см. utils.get_all_candles
                )
                # print(r)

                df = get_info().create_df(r.candles)

                # print(df[['time', 'close']].tail(50))
                return df

        except RequestError as e:
            print(str(e))

    def create_df(self, candles: [HistoricCandle]):
        df = DataFrame([{
            # +3 часа
            'Time': c.time + timedelta(hours=3),
            'Volume': c.volume,
            'Open': get_info().cast_money(c.open),
            'Close': get_info().cast_money(c.close),
            'High': get_info().cast_money(c.high),
            'Low': get_info().cast_money(c.low),
        } for c in candles])
        return df


    def cast_money(self, v):
        return v.units + v.nano / 1e9


# figi = 'TCS10A101X50'
figi = 'BBG004730N88'
proch = 0
days = 365
df = pd.DataFrame({})
for data in range(days, 1, -1):
    df = pd.concat([df, get_info().get_price(figi, data)], axis=0, ignore_index=True)
    # df += get_info().get_price(figi, data)
    # print(len(get_info().get_price(figi, data)))
    proch += 1
    print(f'готово на {proch}/{days}')

# df.drop(df.columns[[0]], axis=1, inplace=True)
print(df)

# сохранение таблицы
csv_file_path = f'SBER_{days}d_15m.csv'
df.to_csv(csv_file_path, index=False)
print(f'CSV file "{csv_file_path}" был успешно создан')