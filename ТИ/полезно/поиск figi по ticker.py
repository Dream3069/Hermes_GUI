from pandas import DataFrame
from tinkoff.invest import Client
from tinkoff.invest.services import InstrumentsService, MarketDataService, InstrumentStatus, InstrumentIdType
import creds


# SBER BBG004730N88
# AFLT BBG004S683W7
# VTBR BBG004730ZJ9
# ALRS BBG004S68B31
# поиск figi по ticker
TICKER = 'ALRS'
# AFLT UGLD
def find_figi():
    with Client(creds.TOKEN) as cl:
        instruments: InstrumentsService = cl.instruments
        market_data: MarketDataService = cl.market_data
        # поиск figi для акций
        # r = instruments.share_by(id_type=InstrumentIdType.INSTRUMENT_ID_TYPE_FIGI, id="BBG004S68B31")
        # print(r)
        r = DataFrame(instruments.shares(
            instrument_status=InstrumentStatus.INSTRUMENT_STATUS_BASE).instruments,
                      columns=['name', 'figi', 'ticker'])
        r = r[r['ticker'] == TICKER]
        print(r)
        """lst = []
        # bonds = облигация, currencies = валюта ,futures = фьючерсы
        # shares = акции ,etfs = фонды
        for method in ['shares', 'bonds', 'etfs']:  # , 'currencies', 'futures']:
            for item in getattr(instruments, method)().instruments:
                lst.append({
                    'ticker': item.ticker,
                    'figi': item.figi,
                    'type': method,
                    'name': item.name})

        df = DataFrame(lst)
        df = df[df['ticker'] == 'AFLT']
        if df.empty:
            print(f"Нет тикера {TICKER}")
            return

        # вся инфа
        # print(df.iloc[0])
        print(df['figi'].iloc[0])"""
if __name__ == '__main__':
    find_figi()