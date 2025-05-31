import matplotlib.pyplot as plt
from pybit.unified_trading import HTTP
import time

def plot_asset_price(symbol: str, interval: int = 60, count: int = 100, category: str = "spot"):
    """
    Строит график цены актива (например, BTCUSDT) на Bybit.

    Параметры:
    - symbol: Торговая пара (напр., "BTCUSDT")
    - interval: Интервал свечей в минутах (1, 5, 15, 60, ...)
    - count: Количество свечей (макс. 1000)
    - category: "spot", "linear" (фьючерсы), "inverse"
    """
    # Подключаемся к API Bybit (публичные данные, ключи не нужны)
    session = HTTP(testnet=True)  # Для mainnet: testnet=False

    try:
        # Получаем свечи (Kline)
        klines = session.get_kline(
            category=category,
            symbol=symbol,
            interval=interval,
            limit=count
        )["result"]["list"]

        # Извлекаем время и цены
        times = []
        prices = []
        for k in klines:
            timestamp = int(k[0]) // 1000  # Время в секундах
            times.append(time.strftime("%Y-%m-%d %H:%M", time.localtime(timestamp)))
            prices.append(float(k[4]))  # Цена закрытия свечи

        # Разворачиваем списки (Bybit возвращает свечи от новых к старым)
        times = times[::-1]
        prices = prices[::-1]

        # Настраиваем график
        plt.figure(figsize=(12, 6))
        plt.plot(times, prices, label=f"{symbol} Price", color="blue")
        plt.title(f"{symbol} Price Chart ({interval}min)")
        plt.xlabel("Time")
        plt.ylabel("Price (USDT)")
        plt.xticks(rotation=45)
        plt.grid(True)
        plt.legend()
        plt.tight_layout()
        plt.show()
        return prices
    except Exception as e:
        print(f"Ошибка: {e}")

# Пример использования
if __name__ == "__main__":
    plot_asset_price("BTCUSDT", interval=15, count=50)  # 15-минутные свечи, 50 последних