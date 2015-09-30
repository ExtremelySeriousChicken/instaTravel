from .sampleInstagram import setup
from flask import request, Flask, render_template, session, redirect, session, redirect, url_for
from flask.ext.bootstrap import Bootstrap
from flask.ext.moment import Moment
from config import config
import requests
from instagram.client import InstagramAPI
from clarifai.client import ClarifaiApi
import requests
import json
from .instagramAPI import *

client_id = "7a70b000e89148c099fadad54d6c7646"
client_secret = "16eea5b495b54a7d89bf33b0418cf1f7"
amadeus_api_key = 'RzGfJPsCmYIRlDmTi6Og2BAYAVviEAdh'
import requests
bootstrap = Bootstrap()
moment = Moment()
class oauth(object):
    def __init__():
        pass

def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(config[config_name])
    config[config_name].init_app(app)
    bootstrap.init_app(app)
    moment.init_app(app)
    # attach routes and custom error pages here

    @app.route('/') 
    def index():
    	return render_template('index.html')

    @app.route('/verified')
    def verified():
        print(url_for('verified'))
        print(access_token )
        return access_token

    @app.route('/data/<code>')
    def findLocation(code):
        print("The code:")
        print(code)

        return render_template('index2.html', code=code)

    @app.route('/instagram_callback')
    def insta():
        data = request.args.get('code')
        return redirect("/data/" + data)

    @app.route('/data/<code>/<airport>')
    def index3(code, airport):
        api = InstagramAPI(access_token=code, client_secret=client_secret)
        locations = list()
        userMediaValue = list()
        result = getUserLikedInformation(userMediaValue, locations)
        print("getUserLikedInfo passed")
        userMediaValue = result[0]
        locations = result[1]
        locations = prepareGeoTagList(userMediaValue, locations)
        print("parepareGeoList passed")
        maxAirport = areaCount(locations)
        tagDict = list()
        result = searchInstagram(userMediaValue, tagDict)
        tagDict = result[1]
        finalReturnedList = result[0]

        print finalReturnedList

        return render_template('index3.html')

    # @app.route('/data2/<code>/<airport>')
    # def index4(code, airport):
    #     return render_template


    @app.route('/try')
    def tryThis():
        return redirect("https://api.instagram.com/oauth/authorize/?client_id=7a70b000e89148c099fadad54d6c7646&redirect_uri=http://localhost:5000/instagram_callback&response_type=code")


    
    return app