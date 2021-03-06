"""module for initializing namespaces
has three namespaces auth,questions and votes"""
from flask import Blueprint
from flask_restplus import Api
from .auth import api as ns1
from .questions import api as ns2
from .votes import api as ns3

authorizations = {
    'apikey': {
        'type': 'apiKey',
        'schema': 'Bearer',
        'in': 'header',
        'header': 'Bearer',
        'name': 'Authorization'
    }
}
apiv1_bp = Blueprint('apiv1', __name__)

api = Api(apiv1_bp,
          title='StackOverFlow-lite API documentation',
          version='1.0',
          description='An api where users can post questions ans answers',
          authorizations=authorizations,
          security='apikey'
          )
api.add_namespace(ns1)
api.add_namespace(ns2)
api.add_namespace(ns3)
