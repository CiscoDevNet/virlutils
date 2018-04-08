from flask import Flask
from flask import render_template


app = Flask(__name__)


@app.route('/')
def swagger_ui(name=None):
    username = app.config['VIRL_USERNAME']
    password = app.config['VIRL_PASSWORD']
    return render_template('index.html', username=username, password=password)


@app.route('/swagger.json')
def swagger_def(name=None):
    host = app.config['VIRL_HOST']
    port = app.config['VIRL_PORT']
    return render_template('swagger.json', host=host, port=port)


if __name__ == "__main__":

    app.run()
