from flask import Blueprint
from flask_restful import Api
from .client import *
from .invoices import *
from .product import *
from .payment import *

api_blueprint = Blueprint("api", __name__, url_prefix='/api')
api = Api(api_blueprint)
api.add_resource(ClientList, "/client/list")
api.add_resource(ClientListById, "/client/list/<id>")
api.add_resource(ClientListByEmail, "/client/list/email/<email>")
api.add_resource(CreateClient, "/client/create")

api.add_resource(InvoiceList, "/invoice/list")
api.add_resource(InvoiceListById, "/invoice/list/<id>")
api.add_resource(InvoiceCreate, "/invoice/create")

api.add_resource(ProductList, "/product/list")
api.add_resource(ProductListById, "/product/list/<id>")

api.add_resource(PaymentsList, "/payment/list")
api.add_resource(PaymentsListById, "/payment/list/<id>")
api.add_resource(CreatePayment, "/payment/create")



