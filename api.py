from futu import *
import traceback

class OrderBookHandler(OrderBookHandlerBase):

    def __init__(self, callback):
        super(OrderBookHandler, self).__init__()
        self.callback = callback

    def on_recv_rsp(self, rsp_pb):
        ret, data = super(OrderBookHandler, self).on_recv_rsp(rsp_pb)

        if ret == RET_OK:
            self.callback(data)

        return RET_OK, data


def get_option_dates(stock_code):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    dates = []

    try:
        ret, data = quote_ctx.get_option_expiration_date(code=stock_code)

        if ret == RET_OK:
            dates = data['strike_time'].values.tolist()
    except:
        traceback.print_exc()

    quote_ctx.close()

    return dates


def get_option_strikes(stock_code, expr_date, option_type):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    strikes = []

    try:
        ret, data = quote_ctx.get_option_chain(code=stock_code, start=expr_date, end=expr_date, option_type=OptionType.CALL if option_type == 'call' else OptionType.PUT)

        if ret == RET_OK:
            for row in data.itertuples():
                strikes.append({
                    'code': row.code,
                    'price': row.strike_price
                })
    except:
        traceback.print_exc()

    quote_ctx.close()

    return strikes


def subscribe_option_price(option_code, callback):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    quote_ctx.unsubscribe_all()
    quote_ctx.set_handler(OrderBookHandler(callback))
    quote_ctx.subscribe([option_code], [SubType.ORDER_BOOK])

    return quote_ctx
