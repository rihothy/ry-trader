from flask import Flask, render_template, jsonify, request
import logging
import time
import json

import api

logging.getLogger('werkzeug').setLevel(logging.ERROR)

app = Flask(__name__)
app.jinja_env.auto_reload = True

quote_time = None
quote_ctx = None
quote_data = {}

@app.route('/')
def index():
    return render_template('index.html')


@app.get('/dates')
def get_option_dates():
    return jsonify(api.get_option_dates(request.args.get('stock-code')))


@app.get('/strikes')
def get_option_strikes():
    return jsonify(api.get_option_strikes(request.args.get('stock-code'), request.args.get('expr-date'), request.args.get('option-type')))


@app.get('/subscribe')
def subscribe():
    global quote_ctx, quote_data, quote_time

    def callback(data):
        global quote_ctx, quote_data, quote_time

        quote_data = data
        print('callback')

        if quote_time is not None and time.time() - quote_time > 3:
            quote_ctx.close()
            quote_time = None
            quote_ctx = None
            quote_data = {}

    if quote_ctx is not None:
        quote_ctx.close()

    quote_data = {}
    quote_time = None

    print('subscribe')
    quote_ctx = api.subscribe_option_price(request.args.get('option-code'), callback)

    return ''


@app.get('/unsubscribe')
def unsubscribe():
    global quote_ctx, quote_data, quote_time

    if quote_ctx is not None:
        quote_ctx.close()
        quote_ctx = None

    quote_data = {}
    quote_time = None

    print('unsubscribe')

    return ''


@app.get('/price')
def get_option_price():
    global quote_time

    quote_time = time.time()

    return jsonify(quote_data)


if __name__ == '__main__':
    app.run('0.0.0.0', 5500, debug=True)
