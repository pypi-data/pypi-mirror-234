import logging
import os

from config import Config
from flask import Flask

from views.auth import auth_page
from views.admin import admin_page
from views.index import index_page

from autonomous import log
from autonomous.assets import build_assets


def create_app():
    app = Flask(os.getenv("APP_NAME", __name__))
    app.config.from_object(Config)
    # log(app.config.get("PORT"))
    #################################################################
    #                             Filters                           #
    #################################################################
    # app.jinja_env.filters['datetime_format'] = datefilters.datetime_format

    #################################################################
    #                             Extensions                        #
    #################################################################

    # - Assets

    # csspath_dir = "static/style/sass/main.scss"
    # cssoutput_dir = "static/style/main.css"
    # jspath_dir = "static/js"
    # jsoutput_dir = "static/main.min.js"
    app.before_request(lambda: build_assets())

    #################################################################
    #                             ROUTES                            #
    #################################################################

    ######################################
    #           Blueprints               #
    ######################################
    app.register_blueprint(index_page)
    app.register_blueprint(auth_page, url_prefix="/auth")
    app.register_blueprint(admin_page, url_prefix="/admin")

    return app
