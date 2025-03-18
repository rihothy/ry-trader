from flask import Flask, render_template, jsonify, request
import config as cfg
import api

app = Flask(__name__)
app.jinja_env.auto_reload = True

@app.route('/')
def index():
    dates = api.get_option_dates()

    return render_template('index.html')


@app.get('/dates')
def get_option_dates():
    cfg.put('code', request.args.get('code'))

    return jsonify(api.get_option_dates())


@app.get('/strikes')
def get_option_strikes():
    cfg.put('code', request.args.get('code'))
    cfg.put('type', request.args.get('type'))
    cfg.put('date', request.args.get('date'))

    return jsonify(api.get_option_strikes())


if __name__ == '__main__':
    app.run('0.0.0.0', 8080, True)