from flask import Flask, render_template, session, redirect, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from config import config
bootstrap = Bootstrap()

moment = Moment()

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    # attach routes and custom error pages here

    @app.route('/')
    def index():
        return '<h1>Welcome!</h1>'

    
    return app