import mplfinance as mpf
import pandas as pd
from pybit.unified_trading import HTTP
from datetime import datetime
import matplotlib.pyplot as plt  # Добавляем импорт


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

        # 2. Проверяем ответ API
        if not response or "result" not in response:
            print("Ошибка: Некорректный ответ API")
            print("Полный ответ:", response)
            return

        klines = response["result"].get("list", [])
        if not klines:
            print("Ошибка: Пустой список свечей")
            return

        print(f"Успешно получено {len(klines)} свечей")
        print("Первая свеча:", klines[0])

        # Подготовка данных
        data = []
        for k in klines:
            try:
                data.append({
                    'time': datetime.fromtimestamp(int(k[0]) / 1000),
                    'open': float(k[1]),
                    'high': float(k[2]),
                    'low': float(k[3]),
                    'close': float(k[4]),
                    'volume': float(k[5])
                })
            except (IndexError, ValueError) as e:
                print(f"Ошибка обработки свечи: {e} | Данные: {k}")

        if not data:
            print("Нет данных для построения графика")
            return

        df = pd.DataFrame(data)
        df = df.iloc[::-1].set_index('time')

        # Настройка стиля
        mc = mpf.make_marketcolors(
            up='g', down='r',
            wick={'up': 'g', 'down': 'r'},
            volume='in'
        )
        style = mpf.make_mpf_style(marketcolors=mc)

        # Построение графика
        mpf.plot(
            df,
            type='candle',
            style=style,
            title=f'{symbol} {interval}min',
            ylabel='Price ($)',
            volume=True,
            figratio=(12, 6),
            show_nontrading=True
        )

        plt.show()  # отображаем график

    except Exception as e:
        print(f"Критическая ошибка: {str(e)}")


# Запуск
if __name__ == "__main__":
    plot_candlestick("BTCUSDT", 60, 200)
    print("График должен отобразиться в отдельном окне")