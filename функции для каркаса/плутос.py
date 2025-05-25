from datetime import timedelta, datetime
from pandas import DataFrame
import asyncio
import time

import numpy as np
import pandas as pd
# t.0Y1j_DXVO4Mx9gBEl2jvHZglLv24law5b8W3WdoQT4R2QbZrdZe2cBpi8Y_uRvQeUF_7V8jIoiOB3ECwr7C-YA
# UNAC NSVZ SELG

class helper():
# класс для нахождения самой эффективной стратегии

    # создание таблицы цен
    async def create_data(self, figi, token):
        lst_price = []
        lst_time = []
        async with AsyncRetryingClient(token, settings=RetryClientSettings(use_retry=True, max_retry_attempt=2)) as client:
            async for candle in client.get_all_candles(
                    figi=figi,
                    from_=now() - timedelta(days=252),
                    interval=CandleInterval.CANDLE_INTERVAL_DAY,
            ):
                lst_price.append(float(candle.open.units + candle.open.nano / 1e9))
                lst_time.append(candle.time)
                # таблица с ценами за день
                data = pd.DataFrame({"time": lst_time, 'Close': lst_price})
            return data
# поиск подходящей стратегии
    def find_strategy(self, data):
        # короткая и длинная скользящая средняя
        short_ma = 5
        long_ma = 12
        # периодичность расчета индекс относительной силы
        rsi_period = 14
        # паттерны когда акция перекуплена перепродана
        rsi_oversold = 30
        rsi_overbought = 70
        # индекс продажи на стратегии поддержки и сопротивления
        sr_sell = 0.8
        sr_buy = 0.3
        # расчет скользящей средней
        data['MA_' + str(short_ma)] = data['Close'].rolling(short_ma).mean()
        data['MA_' + str(long_ma)] = data['Close'].rolling(long_ma).mean()
        # расчет доходности
        data['return'] = data['Close'].pct_change()
        # среднее движение цен верх и вниз
        data['UP'] = np.maximum(data['Close'].diff(), 0)
        data['DOWN'] = np.maximum(-data['Close'].diff(), 0)
        # относительная сила
        data['RS'] = data['UP'].rolling(rsi_period).mean() / data['DOWN'].rolling(rsi_period).mean()
        # индекс относительной силы
        data['RSI'] = 100 - 100 / (1 + data['RS'])
        # поддержка и сопротивление
        data['S&R'] = (data['Close'] / (10 ** np.floor(np.log10(data['Close'])))) % 1

        # когда вступать в торговлю
        start = max(long_ma, rsi_period)
        # тактика MACD(пересечение скользящих средних) 1 покупай -1 продавай
        data['MACD_signal'] = 2 * (data['MA_' + str(short_ma)] > data['MA_' + str(long_ma)]) - 1
        data['RSI_signal'] = 1 * (data['RSI'] < rsi_oversold) - 1 * (data['RSI'] > rsi_overbought)
        data['S&R_signal'] = 1 * (data['S&R'] < sr_buy) - 1 * (data['S&R'] > sr_sell)
        # перевод сигнал в доходность и симулировать наших стратегий
        MACD_return = np.array(data['return'][start + 1:]) * np.array(data['MACD_signal'][start:-1])
        RSI_return = np.array(data['return'][start + 1:]) * np.array(data['RSI_signal'][start:-1])
        SR_return = np.array(data['return'][start + 1:]) * np.array(data['S&R_signal'][start:-1])
        # средние показатели доходности в год (число 252 это число торговых дней в году)
        MACD = np.prod(1 + MACD_return) ** (252 / len(MACD_return))
        RSI = np.prod(1 + RSI_return) ** (252 / len(RSI_return))
        SR = np.prod(1 + SR_return) ** (252 / len(SR_return))
        # расчет годового риска
        MACD_risk = np.std(MACD_return) * (252) ** (1 / 2)
        RSI_risk = np.std(RSI_return) * (252) ** (1 / 2)
        SR_risk = np.std(SR_return) * (252) ** (1 / 2)

        # количество строк в таблице без ограничений
        pd.set_option('display.max_rows', None)
        # количество столбцов в таблице без ограничений
        pd.set_option('display.max_columns', None)
        # текст в ячейке отображается полностью вне зависимости от длины
        pd.set_option('display.max_colwidth', None)
        print(data)
        print(f'доходность и риск стратегии скользящих средних {str(round(MACD * 100, 2))} % и {str(round(MACD_risk * 100, 2))} %')
        print(f'доходность и риск стратегии RSI {str(round(RSI * 100, 2))} % и {str(round(RSI_risk * 100, 2))} %')
        print(f'доходность и риск стратегии поддержка и сопротивления {str(round(SR * 100, 2))} % и {str(round(SR_risk * 100, 2))} %')

        lst_name = ["MACD_signal", "RSI_signal", "S&R_signal"]
        lst_profit = [round(MACD * 100, 2), round(RSI * 100, 2), round(SR * 100, 2)]
        lst_risk = [round(MACD_risk * 100, 2), round(RSI_risk * 100, 2), round(SR_risk * 100, 2)]
        # ищет индекс среднего по риску
        index = 3 - (lst_risk.index(min(lst_risk)) + lst_risk.index(max(lst_risk)))
        for i in range(3):
            if lst_profit[index] > 100 and lst_profit[lst_risk.index(min(lst_risk))] < lst_profit[index] < lst_profit[lst_risk.index(max(lst_risk))]:
                return lst_name[index], lst_profit[index], lst_risk[index], data


    def my_money_bust(self, data, name):
        # 1 покупай -1 продавай
        global buy_or_sell
        """print(data["Close"].iloc[-1])
        print(data[name])"""
        # расчет покупки
        # data[name].iloc[-1] возвращает последний элемент
        if (data[name].iloc[-1] == 1) and (buy_or_sell is True):
            print(f"купить")

            buy_or_sell = False
        # расчет продажи
        elif (data[name].iloc[-1] == -1) and (buy_or_sell is False):
            print(f"продать")
            buy_or_sell = True