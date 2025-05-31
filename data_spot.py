import mplfinance as mpf
import pandas as pd
from pybit.unified_trading import HTTP
from datetime import datetime
import matplotlib.pyplot as plt  # Добавляем импорт
import all_spot
import datetime

def plot_candlestick(symbol: str = "BTCUSDT", interval: int = 15, count: int = 100):
    try:
        # Получаем данные
        session = HTTP(testnet=True)
        response = session.get_kline(
            category="spot",
            symbol=symbol,
            interval=interval,
            limit=count
        )
        print(response)
        # 2. Проверяем ответ API
        if not response or "result" not in response:
            print("Ошибка: Некорректный ответ API")
            print("Полный ответ:", response)
            return

        klines = response["result"].get("list", [])
        if not klines:
            print("Ошибка: Пустой список свечей")
            return

        print(f"Успешно получено {len(klines)} свечей для {symbol}")
        # вывод первой свечи
        # print("Первая свеча:", klines[0])

        # Подготовка данных
        data = []
        for k in klines:
            try:
                data.append({
                    'data': datetime.datetime.fromtimestamp(float(k[0]) / 1000.0),
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4])
                })
            except (IndexError, ValueError) as e:
                print(f"Ошибка обработки свечи: {e} | Данные: {k}")

        if not data:
            print("Нет данных для построения графика")
            return

        df = pd.DataFrame(data)

        return df
    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")


# Запуск
if __name__ == "__main__":
    all_spot = all_spot.main()
    print(all_spot)
    # инетервал
    interval = 60
    # кол-во свечей
    count = 200
    # for name in all_spot:
        # print(plot_candlestick(name, 60, 200))
    print(plot_candlestick("BTCUSDT", 60, 200))

