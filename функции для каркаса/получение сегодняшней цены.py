from pybit.unified_trading import HTTP


class BybitPriceChecker:
    def __init__(self, api_key: str = "", api_secret: str = "", testnet: bool = True):
        """Инициализация с возможностью работы без API ключей (только публичные данные)"""
        self.client = HTTP(
            api_key=api_key,
            api_secret=api_secret,
            testnet=testnet
        )

    def get_price(self, symbol: str) -> float:
        """
        Получает текущую цену актива
        :param symbol: Название пары (BTCUSDT, ETHUSDT и т.д.)
        :return: Текущая цена или 0 при ошибке
        """
        try:
            # Пробуем сначала спотовый рынок
            response = self.client.get_tickers(category="spot", symbol=symbol)
            if response['retCode'] == 0:
                return float(response['result']['list'][0]['lastPrice'])

            # Если нет на споте, пробуем линейные фьючерсы
            response = self.client.get_tickers(category="linear", symbol=symbol)
            return float(response['result']['list'][0]['lastPrice'])
        except Exception as e:
            print(f"Ошибка получения цены для {symbol}: {e}")
            return 0

    def print_price(self, symbol: str):
        """Выводит форматированную информацию о цене"""
        price = self.get_price(symbol)
        if price > 0:
            print(f"🏷 {symbol}: ${price:,.4f}")
        else:
            print(f"❌ Не удалось получить цену для {symbol}")


# Пример использования
if __name__ == "__main__":
    # Инициализация (ключи не обязательны для публичных данных)
    checker = BybitPriceChecker(testnet=True)

    # Проверка цены
    checker.print_price("BTCUSDT")  # Спот
    checker.print_price("ETHUSDT")  # Спот
    checker.print_price("XRPUSDT")  # Спот
    checker.print_price("SOLUSDT")  # Спот