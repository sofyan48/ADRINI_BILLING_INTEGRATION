from flask_restful import Resource, reqparse
from app.helper.rest import *
from app.libs import utils
from app.helper.rest import response
from app.models import model as db

class ProductList(Resource):
    def get(self):
        try:
            client_data = utils.get_ninja(api="products")
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=client_data['data'])

class ProductListById(Resource):
    def get(self, id):
        try:
            client_data = utils.get_ninja(api="products/"+id)
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=client_data['data'])