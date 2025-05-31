from pybit.unified_trading import HTTP
import os

def get_all_trading_symbols(api_key=None, api_secret=None, testnet=True):
    """
    Получает список всех торговых пар на Bybit (спот, линейные фьючерсы, инверсные фьючерсы).

    :param api_key: API-ключ (необязательно для публичных данных)
    :param api_secret: API-секрет (необязательно для публичных данных)
    :param testnet: Использовать тестовую сеть (True/False)
    :return: Словарь с символами по категориям
    """
    session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)

    symbols_data = {}

    # Получаем спотовые пары (spot)
    try:
        spot_symbols = session.get_instruments_info(category="spot")["result"]["list"]
        symbols_data["spot"] = [s["symbol"] for s in spot_symbols]
    except Exception as e:
        print(f"Ошибка при получении спотовых пар: {e}")

    # Получаем линейные фьючерсы (USDT-перипетуальные)
    try:
        linear_symbols = session.get_instruments_info(category="linear")["result"]["list"]
        symbols_data["linear_perpetual"] = [s["symbol"] for s in linear_symbols]
    except Exception as e:
        print(f"Ошибка при получении линейных фьючерсов: {e}")

    # Получаем инверсные фьючерсы (BTC/USD и др.)
    try:
        inverse_symbols = session.get_instruments_info(category="inverse")["result"]["list"]
        symbols_data["inverse_futures"] = [s["symbol"] for s in inverse_symbols]
    except Exception as e:
        print(f"Ошибка при получении инверсных фьючерсов: {e}")

    return symbols_data


# Пример использования
if __name__ == "__main__":
    api_key = os.getenv('12cfLqsr1J72rSAUIe')
    api_secret = os.getenv('JKVgRkBOMh6iEJJziAIIHvCAIoa0xmosG1S0')
    trading_symbols = get_all_trading_symbols(api_key, api_secret, testnet=True)  # Для mainnet → testnet=False

    print("🔹Спотовые пары (Spot):")
    print(trading_symbols.get("spot", []))

    print("\n🔹Линейные перпетуальные контракты (USDT):")
    print(trading_symbols.get("linear_perpetual", []))

    print("\n🔹Инверсные фьючерсы (BTCUSD, ETHUSD и др.):")
    print(trading_symbols.get("inverse_futures", []))