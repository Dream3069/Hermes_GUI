from pybit.unified_trading import HTTP


def trade_bybit(
        symbol: str,
        side: str,  # "Buy" или "Sell"
        order_type: str,  # "Market" или "Limit"
        quantity: float,
        price: float = None,  # Нужно для лимитных ордеров
        api_key: str = "YOUR_API_KEY",
        api_secret: str = "YOUR_API_SECRET",
        testnet: bool = True,  # True = тестовая сеть, False = реальный рынок
        category: str = "spot"  # "spot", "linear" (фьючерсы), "inverse"
) -> dict:
    """
    Размещает ордер на Bybit (покупка/продажа).

    Параметры:
    - symbol: Торговая пара (напр., "BTCUSDT")
    - side: "Buy" (купить) или "Sell" (продать)
    - order_type: "Market" (рыночный) или "Limit" (лимитный)
    - quantity: Количество (в базовой валюте, напр., 0.01 BTC)
    - price: Цена (только для лимитных ордеров)
    - api_key, api_secret: Ключи API Bybit
    - testnet: Тестовая сеть (True/False)
    - category: "spot" (спот), "linear" (USDT-фьючерсы), "inverse" (BTCUSD и др.)

    Возвращает:
    - Ответ от Bybit API (успешный ордер или ошибка)
    """
    # Подключаемся к API
    session = HTTP(
        api_key=api_key,
        api_secret=api_secret,
        testnet=testnet
    )

    # Параметры ордера
    order_params = {
        "category": category,
        "symbol": symbol,
        "side": side,
        "orderType": order_type,
        "qty": str(quantity),
    }

    # Для лимитного ордера добавляем цену
    if order_type == "Limit":
        order_params["price"] = str(price)

    try:
        # Размещаем ордер
        response = session.place_order(**order_params)
        return response
    except Exception as e:
        return {"error": str(e)}


# Пример использования
if __name__ == "__main__":
    # Пример рыночной покупки BTCUSDT (спот)
    print("🟢 Покупаем BTCUSDT (рыночный ордер):")
    market_buy = trade_bybit(
        symbol="BTCUSDT",
        side="Buy",
        order_type="Market",
        quantity=0.001,  # Купить 0.001 BTC
        category="spot"
    )
    print(market_buy)

    # Пример лимитной продажи ETHUSDT (фьючерсы)
    print("\n🔴 Продаем ETHUSDT (лимитный ордер):")
    limit_sell = trade_bybit(
        symbol="ETHUSDT",
        side="Sell",
        order_type="Limit",
        quantity=0.1,  # Продать 0.1 ETH
        price=3500.0,  # Цена продажи
        category="linear"
    )
    print(limit_sell)