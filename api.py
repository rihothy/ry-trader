import config as cfg
from futu import *
import traceback

def get_option_dates():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    dates = []

    try:
        ret, data = quote_ctx.get_option_expiration_date(code='US.%s' % (cfg.get()['code']))

        if ret == RET_OK:
            dates = data['strike_time'].values.tolist()
    except:
        traceback.print_exc()

    quote_ctx.close()

    return dates


def get_option_strikes():
    quote_ctx = OpenQuoteContext(host='127.0.0.1', port=11111)
    info = cfg.get()
    strikes = []

    try:
        ret, data = quote_ctx.get_option_chain(code='US.%s' % (info['code']), start=info['date'], end=info['date'], option_type=OptionType.CALL if info['type'] == 'call' else OptionType.PUT)

        if ret == RET_OK:
            strikes = data['strike_price'].values.tolist()
    except:
        traceback.print_exc()

    quote_ctx.close()

    return strikes


if __name__ == '__main__':
    print(get_option_strikes())