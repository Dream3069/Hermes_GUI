from datetime import datetime, timedelta, timezone

from pandas import DataFrame

from tinkoff.invest import Client, RequestError, CandleInterval, HistoricCandle

import creds
import pandas as pd

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)


class get_info():
    def get_price(self, figi, days=361):
        try:
            with Client(creds.TOKEN) as client:
                r = client.market_data.get_candles(
                    figi=figi,
                    from_=datetime.now(timezone.utc) - timedelta(days=days),
                    to=datetime.now(timezone.utc),
                    interval=CandleInterval.CANDLE_INTERVAL_DAY  # см. utils.get_all_candles
                )
                # print(r)

                df = get_info().create_df(r.candles)

                # print(df[['time', 'close']].tail(50))
                return df

        except RequestError as e:
            print(str(e))

    def create_df(self, candles: [HistoricCandle]):
        df = DataFrame([{
            # +5 часа
            'time': c.time + timedelta(hours=5),
            'volume': c.volume,
            'open': get_info().cast_money(c.open),
            'close': get_info().cast_money(c.close),
            'high': get_info().cast_money(c.high),
            'low': get_info().cast_money(c.low),
        } for c in candles])
        return df


    def cast_money(self, v):
        return v.units + v.nano / 1e9


# figi = 'TCS10A101X50'
# print(get_info().get_price(figi))
# print(len(get_info().get_price(figi)))
