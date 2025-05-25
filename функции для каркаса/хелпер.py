from datetime import timedelta, datetime
import pandas as pd
import numpy as np
from pybit.unified_trading import HTTP


class BybitDataFetcher:
    def __init__(self, api_key: str = "", api_secret: str = "", testnet: bool = True):
        self.client = HTTP(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet
        )

    def get_klines(self, symbol: str, interval: int = 15, days: int = 2) -> pd.DataFrame:
        """Получает свечные данные с Bybit"""
        end_time = datetime.now()
        start_time = end_time - timedelta(days=days)

        try:
            response = self.client.get_kline(
                category="spot",
                symbol=symbol,
                interval=interval,
                start=int(start_time.timestamp() * 1000),
                end=int(end_time.timestamp() * 1000),
                limit=200
            )

            if response['retCode'] != 0:
                raise Exception(f"API error: {response['retMsg']}")

            klines = response['result']['list']

            data = []
            for k in klines:
                data.append({
                    'time': datetime.fromtimestamp(int(k[0]) / 1000),
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[5])
                })

            df = pd.DataFrame(data)
            df.set_index('time', inplace=True)
            return df.sort_index()

        except Exception as e:
            print(f"Error fetching data for {symbol}: {e}")
            return pd.DataFrame()


class StrategyAnalyzer:
    def __init__(self):
        self.short_ma = 5
        self.long_ma = 12
        self.rsi_period = 14
        self.rsi_oversold = 30
        self.rsi_overbought = 70
        self.sr_sell = 0.8
        self.sr_buy = 0.3

    def calculate_indicators(self, data: pd.DataFrame) -> pd.DataFrame:
        """Рассчитывает технические индикаторы"""
        # Скользящие средние
        data[f'MA_{self.short_ma}'] = data['close'].rolling(self.short_ma).mean()
        data[f'MA_{self.long_ma}'] = data['close'].rolling(self.long_ma).mean()

        # Доходность
        data['return'] = data['close'].pct_change()

        # RSI
        delta = data['close'].diff()
        gain = delta.where(delta > 0, 0)
        loss = -delta.where(delta < 0, 0)

        avg_gain = gain.rolling(self.rsi_period).mean()
        avg_loss = loss.rolling(self.rsi_period).mean()

        rs = avg_gain / avg_loss
        data['RSI'] = 100 - (100 / (1 + rs))

        # Support & Resistance
        data['S&R'] = (data['close'] / (10 ** np.floor(np.log10(data['close'])))) % 1

        # Сигналы
        start = max(self.long_ma, self.rsi_period)
        data['MACD_signal'] = 2 * (data[f'MA_{self.short_ma}'] > data[f'MA_{self.long_ma}']) - 1
        data['RSI_signal'] = 1 * (data['RSI'] < self.rsi_oversold) - 1 * (data['RSI'] > self.rsi_overbought)
        data['S&R_signal'] = 1 * (data['S&R'] < self.sr_buy) - 1 * (data['S&R'] > self.sr_sell)

        return data

    def evaluate_strategies(self, data: pd.DataFrame) -> dict:
        """Оценивает эффективность стратегий"""
        start = max(self.long_ma, self.rsi_period)

        # Рассчитываем доходности стратегий
        strategies = {
            'MACD': data['MACD_signal'][start:-1] * data['return'][start + 1:],
            'RSI': data['RSI_signal'][start:-1] * data['return'][start + 1:],
            'S&R': data['S&R_signal'][start:-1] * data['return'][start + 1:]
        }

        results = {}

        for name, returns in strategies.items():
            annual_return = np.prod(1 + returns) ** (365 / len(returns)) - 1
            annual_risk = np.std(returns) * np.sqrt(365)
            sharpe = annual_return / annual_risk if annual_risk != 0 else 0


            results[name] = {
                'return': annual_return,
                'risk': annual_risk,
                'sharpe': sharpe
            }

        return results


class TradingHelper:
    def __init__(self, api_key: str = "", api_secret: str = "", testnet: bool = True):
        self.data_fetcher = BybitDataFetcher(api_key, api_secret, testnet)
        self.analyzer = StrategyAnalyzer()
        self.buy_or_sell = True

    async def analyze_symbol(self, symbol: str):
        print(f"\nАнализируем {symbol}...")

        # Получаем данные
        data = self.data_fetcher.get_klines(symbol)
        if data.empty:
            print("Не удалось получить данные")
            return

        # Рассчитываем индикаторы
        data = self.analyzer.calculate_indicators(data)

        # Оцениваем стратегии
        results = self.analyzer.evaluate_strategies(data)

        # Выводим результаты
        print("\nРезультаты стратегий:")
        for name, metrics in results.items():
            print(f"{name}:")
            print(f"  Доходность: {metrics['return'] * 100:.2f}%")
            print(f"  Риск: {metrics['risk'] * 100:.2f}%")
            print(f"  Коэф. Шарпа: {metrics['sharpe']:.2f}")

        # Выбираем лучшую стратегию
        best_strategy = max(results.items(), key=lambda x: x[1]['sharpe'])


        print(f"\nЛучшая стратегия: {best_strategy[0]} (Шарп: {best_strategy[1]['sharpe']:.2f})")

        # Генерируем торговый сигнал
        last_signal = data[f'{best_strategy[0]}_signal'].iloc[-1]
        if last_signal == 1 and self.buy_or_sell:
            print("\nСигнал: ПОКУПАТЬ")
            self.buy_or_sell = False
        elif last_signal == -1 and not self.buy_or_sell:
            print("\nСигнал: ПРОДАВАТЬ")
            self.buy_or_sell = True
        else:
            print("\nСигнал: ОЖИДАТЬ")

        return data


# Пример использования
if __name__ == "__main__":
    # Инициализация (можно без API ключей для публичных данных)
    helper = TradingHelper(testnet=True)

    # Запрашиваем у пользователя символ
    symbol = input("Введите торговую пару (например BTCUSDT): ").strip().upper()

    # Запускаем анализ
    import asyncio

    data = asyncio.run(helper.analyze_symbol(symbol))

    # Выводим последние 5 свечей с индикаторами
    if not data.empty:
        print("\nПоследние 5 свечей:")
        print(data.tail()[['close', f'MA_{helper.analyzer.short_ma}',
                           f'MA_{helper.analyzer.long_ma}', 'RSI', 'S&R',
                           'MACD_signal', 'RSI_signal', 'S&R_signal']])
