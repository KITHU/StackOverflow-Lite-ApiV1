from flask import Flask
from flask_restplus import Api, namespace
from flask_restplus import model
from flask_restplus import fields
from flask_restplus import Resource
from flask_restplus import reqparse
from flask_jwt_extended import JWTManager
from flask_cors import CORS

# local import
from instance.config import app_config


def create_app(config_name):
    app = Flask(__name__)
    app.config.from_object(app_config[config_name])
    jwt = JWTManager(app)
    CORS(app)
    jwt._set_error_handler_callbacks(app)
    from app.apis import apiv1_bp
    app.register_blueprint(apiv1_bp, url_prefix='/api/v1')
    return app
