from flask import Flask, render_template, jsonify, request
import logging
import time

import api

logging.getLogger('werkzeug').setLevel(logging.ERROR)

quote_ctx = None
app = Flask(__name__)
app.jinja_env.auto_reload = True

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/dates')
def get_option_dates():
    return jsonify(api.get_option_dates(request.args.get('stock-code')))


@app.get('/strikes')
def get_option_strikes():
    return jsonify(api.get_option_strikes(request.args.get('stock-code'), request.args.get('expr-date'), request.args.get('option-type')))


@app.get('/price')
def get_option_price():
    return jsonify(api.get_option_price(request.args.get('option-code'), quote_ctx))


@app.get('/subscribe')
def subscribe():
    global quote_ctx

    if quote_ctx is not None:
        quote_ctx.unsubscribe_all()
        quote_ctx.close()

    print('subscribe')
    quote_ctx = api.subscribe_option_price(request.args.get('option-code'))

    return ''


@app.get('/unsubscribe')
def unsubscribe():
    global quote_ctx

    if quote_ctx is not None:
        quote_ctx.unsubscribe_all()
        quote_ctx.close()
        quote_ctx = None

    print('unsubscribe')

    return ''


if __name__ == '__main__':
    app.run('0.0.0.0', 5500, debug=True)
