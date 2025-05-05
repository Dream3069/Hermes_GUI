from tinkoff.invest import Client
from pandas import DataFrame
from tinkoff.invest.services import InstrumentsService
# t.0Y1j_DXVO4Mx9gBEl2jvHZglLv24law5b8W3WdoQT4R2QbZrdZe2cBpi8Y_uRvQeUF_7V8jIoiOB3ECwr7C-YA
# UNAC NSVZ SELG

# класс для получения нужных значений
class find_info():
    # функция для получения токена
    def get_token(self):
        with open('bot_invest_date_token.txt', 'r+') as text_date:
            lst_info = text_date.readline()
            # проверка на пустой список
            if len(lst_info.split(" ")) != 2:
                # получение данных если список оказался пустым
                token = input('ведите токен от вашего аккаунта: ')
                with Client(token) as client:
                    # получение id аккаунта
                    account_id = client.users.get_accounts()
                # очистка документа
                text_date.seek(0)
                # запись документа
                text_date.write(f"{token} {account_id.accounts[0].id}")
                return token, account_id
            else:
                # вывод данных если список оказался не пустым
                lst_info = lst_info.split(" ")
                token = lst_info[0]
                account_id = lst_info[1]
                return token, account_id

    # функция для получения тикера
    def get_ticker(self):
        with open('bot_invest_date_ticker.txt', 'r+') as text_date:
            lst_info = text_date.readline()
            # проверка на пустой список
            if not lst_info:
                # получение данных если список оказался пустым
                ticker = input('ведите тикер акции: ')
                # запись документа
                text_date.write(f"{ticker}")
                return ticker.split(" ")
            else:
                # вывод данных если список оказался не пустым
                return lst_info.split(" ")

    # функция для получения фиги
    def get_figi(self):
        with open('bot_invest_date_figi.txt', 'r+') as text_date:
            lst_info = text_date.readline()
            # проверка на пустой список
            if not lst_info:
                # получение данных если список оказался пустым
                with Client(find_info().get_token()[0]) as cl:
                    instruments: InstrumentsService = cl.instruments
                    lst = []
                    lst_figi = []
                    str_figi = ""
                    for method in ['shares', 'etfs']:  # ,'bonds', 'currencies', 'futures']:
                        for item in getattr(instruments, method)().instruments:
                            lst.append({
                                'ticker': item.ticker,
                                'figi': item.figi,
                                'type': method,
                                'name': item.name,
                            })
                    for i in range(len(find_info.get_ticker(self))):
                        df = DataFrame(lst)
                        df = df[df['ticker'] == find_info.get_ticker(self)[i]]
                        # если акция пропала
                        if df.empty:
                            print(f"Нет тикера {find_info.get_ticker(self)[i]}")
                        else:
                            lst_figi.append(df['figi'].iloc[0])
                            str_figi = f"{str_figi} {df['figi'].iloc[0]}"
                    # запись документа
                    text_date.write(str_figi[1:])
                return lst_figi
            else:
                # вывод данных если список оказался не пустым
                return lst_info.split()


print(find_info().get_token())
print(find_info().get_figi())
