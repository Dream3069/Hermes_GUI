import os
from pybit import exceptions
from pybit.unified_trading import HTTP
import pandas as pd
from pandas import DataFrame

pd.set_option('display.max_rows', 500)
pd.set_option('display.max_columns', 500)
pd.set_option('display.width', 1000)

API_KEY = "12cfLqsr1J72rSAUIe"
SECRET_KEY = "JKVgRkBOMh6iEJJziAIIHvCAIoa0xmosG1S0"

def log_limits(headers : dict):
    print(f"Limits  {headers.get('X-Bapi-Limit-Status')} / {headers.get('X-Bapi-Limit')}")

def assets(cl : HTTP):
    r, _, h = cl.get_wallet_balance(accountType="UNIFIED")
    r = r.get('result', {}).get('list', [])[0]

    total_balance = float(r.get('totalWalletBalance', '0.0'))
    coins = [f"{float(c.get('walletBalance', '0.0')):>12.6f} {c.get('coin'):>12}" for c in r.get('coin', [])]

    print("\n".join(coins))
    print(f"---\nTotal: {total_balance:>18.2f}\n")

    log_limits(h)


def main():

    cl = HTTP(
        api_key=API_KEY,
        api_secret=SECRET_KEY,
        recv_window=60000,
        return_response_headers=True,
    )

    try:
        # r = cl.get_executions(category='linear', limit=10)
        # print(r)

        # вывод всех активов
        assets(cl)


    except exceptions.InvalidRequestError as e:
        print("ByBit Request Error", e.status_code, e.message, sep=" | ")
    except exceptions.FailedRequestError as e:
        print("ByBit Request Failed", e.status_code, e.message, sep=" | ")
    except Exception as e:
        print(e)


if __name__ == '__main__':
    main()