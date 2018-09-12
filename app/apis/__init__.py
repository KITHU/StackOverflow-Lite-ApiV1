from flask import Blueprint
from flask_restplus import Api
from .auth import api as ns1
from .questions import api as ns2
from .votes import api as ns3

authorization = {
    'apiKey': {
        'type': 'apiKey',
        'in': 'header',
        'name': 'Authorization'
    }
}
apiv1_bp = Blueprint('apiv1', __name__)

api = Api(apiv1_bp,
          title='StackOverFlow-lite API documentation',
          version='1.0',
          description='An api where users can post questions ans answers',
          authorizations=authorization
          )

api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
