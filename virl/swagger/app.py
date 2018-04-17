from flask import Flask
from flask import render_template
import os

app = Flask(__name__)


@app.route('/')
def swagger_ui(name=None):
    username = os.environ['VIRL_SWAGGER_USERNAME']
    password = os.environ['VIRL_SWAGGER_PASSWORD']
    return render_template('index.html', username=username, password=password)


@app.route('/swagger.json')
def swagger_def(name=None):
    host = os.environ['VIRL_SWAGGER_HOST']
    port = os.environ['VIRL_SWAGGER_PORT']
    return render_template('swagger.json', host=host, port=port)
