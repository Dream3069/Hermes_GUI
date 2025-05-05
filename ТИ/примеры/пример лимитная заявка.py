FIGI = "TCS10A101X50"
from datetime import datetime
from tinkoff.invest import Client, RequestError, OrderType, OrderDirection, Quotation
import creds


def cast_money(v):
    return v.units + v.nano / 1e9


def run():
    try:
        with Client(creds.TOKEN) as client:

            """book = client.market_data.get_order_book(figi=FIGI, depth=50)
            print(book)
            # bids = [cast_money(p.price) for p in book.bids] # покупатели
            # asks = [cast_money(p.price) for p in book.asks] # продавцы
            # print(bids, asks, sep="\n")
            fast_price_sell, fast_price_buy = book.asks[0], book.bids[0] # центр стакана, мин сопротивление
            best_price_sell, best_price_buy = book.asks[-1], book.bids[-1]  # края стакана, макс сопротивление
            print(fast_price_sell, fast_price_buy)
            print(best_price_sell, best_price_buy) # выводит всю инфу
            print(best_price_sell.price, best_price_buy.price) # выводит только цену"""

            # выводит инфу про не совершенные сделки
            orders = client.orders.get_orders(account_id=creds.account_id).orders
            print(orders)
            # client.orders.get_order_state
            # не исполненные заявки можно отменить
            order_id = orders[0].order_id
            print("Lets cancel order w id %s" % order_id)

            r = client.orders.cancel_order(account_id=creds.account_id, order_id=order_id)
            print(r)

            """r = client.orders.post_order(
                order_id=str(datetime.utcnow().timestamp()),
                figi=FIGI,
                price=Quotation(units=6, nano=360000000),
                quantity=1,
                account_id=creds.account_id,
                direction=OrderDirection.ORDER_DIRECTION_BUY,
                order_type=OrderType.ORDER_TYPE_LIMIT
            )
            print(r)"""

    except RequestError as e:
        print(e)

run()
