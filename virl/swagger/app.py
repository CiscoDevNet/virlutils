from flask import Flask
from flask import render_template
import os
import gunicorn.app.base
from gunicorn.six import iteritems


class StandaloneApplication(gunicorn.app.base.BaseApplication):

    def __init__(self, app, options=None):
        self.options = options or {}
        self.application = app
        super(StandaloneApplication, self).__init__()

    def load_config(self):
        config = dict([(key, value) for key, value in iteritems(self.options)
                       if key in self.cfg.settings and value is not None])
        for key, value in iteritems(config):
            self.cfg.set(key.lower(), value)

    def load(self):
        return self.application


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


if __name__ == "__main__":

    app.run()
