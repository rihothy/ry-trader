from futu import *
import traceback

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
            strikes = [{'code': row.code, 'price': row.strike_price} for row in data.itertuples()]
    except:
        traceback.print_exc()

    quote_ctx.close()

    return strikes


def get_option_price(option_code, quote_ctx):
    if quote_ctx is None:
        return {}

    ret, data = quote_ctx.get_order_book(option_code, num=1)

    if ret != RET_OK:
        return {}

    return data


def subscribe_option_price(option_code):
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)

    quote_ctx.unsubscribe_all()
    quote_ctx.subscribe([option_code], [SubType.ORDER_BOOK], subscribe_push=True)

    return quote_ctx
