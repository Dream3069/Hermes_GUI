from pybit.unified_trading import HTTP
import pandas as pd
from datetime import datetime
import os
from typing import List, Dict, Optional


class BybitSpotMarket:
    def __init__(self, api_key: Optional[str] = None, api_secret: Optional[str] = None, testnet: bool = True):
        """
        Инициализация клиента для работы со спотовым рынком Bybit.

        :param api_key: API-ключ (необязательно для публичных данных)
        :param api_secret: API-секрет (необязательно для публичных данных)
        :param testnet: Использовать тестовую сеть (True/False)
        """
        self.session = HTTP(api_key=api_key, api_secret=api_secret, testnet=testnet)
        self.spot_symbols = []

    def fetch_all_spot_symbols(self) -> List[str]:
        """
        Получает все доступные спотовые пары на Bybit.

        :return: Список символов
        """
        try:
            response = self.session.get_instruments_info(category="spot")
            if response.get("retCode") == 0 or response.get("ret_code") == 0:
                # Обрабатываем оба возможных формата ответа
                result = response.get("result", {})
                if isinstance(result, list):
                    # Новый формат ответа
                    self.spot_symbols = [item["symbol"] for item in result]
                else:
                    # Старый формат ответа
                    self.spot_symbols = [item["symbol"] for item in result.get("list", [])]
                return self.spot_symbols
            else:
                error_msg = response.get("retMsg", response.get("ret_msg", "Unknown error"))
                print(f"Ошибка: {error_msg}")
                return []
        except Exception as e:
            print(f"Ошибка при получении спотовых пар: {str(e)}")
            return []

    def display_spot_symbols(self):
        """Выводит все доступные спотовые пары."""
        if not self.spot_symbols:
            print("Сначала загрузите спотовые пары с помощью fetch_all_spot_symbols()")
            return
        print("\n" + "="*50)
        print(f"Доступные спотовые пары ({len(self.spot_symbols)}):")
        print("="*50)

        # Выводим по 10 символов в строке
        for i in range(0, len(self.spot_symbols), 10):
            print(", ".join(self.spot_symbols[i:i+10]))



def main():
    # Инициализация (API ключи можно задать через переменные окружения)
    api_key = os.getenv('12cfLqsr1J72rSAUIe')
    api_secret = os.getenv('JKVgRkBOMh6iEJJziAIIHvCAIoa0xmosG1S0')

    market = BybitSpotMarket(api_key, api_secret, testnet=True)

    # Загружаем все спотовые пары
    # print("Загрузка спотовых пар...")
    # print(market.fetch_all_spot_symbols())
    # market.display_spot_symbols()
    return market.fetch_all_spot_symbols()


if __name__ == "__main__":
    main()