from flask_restful import Resource, reqparse
from app.helper.rest import *
from app.libs import utils
from app.helper.rest import response
from app.models import model as db

class PaymentsList(Resource):
    def get(self):
        try:
            client_data = utils.get_ninja(api="payments")
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=client_data['data'])

class PaymentsListById(Resource):
    def get(self, id):
        try:
            client_data = utils.get_ninja(api="payments/"+id)
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=client_data['data'])

class CreatePayment(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('invoice_id', type=str, required=True)
        parser.add_argument('amount', type=str, required=True)
        args = parser.parse_args()
        data_payment = {
            "invoice_id": args['invoice_id'],
            "amount": args['amount']
        }
        try:
            payments_data = utils.post_ninja("payments/", data_payment)
        except Exception as e:
            return response(401, message=str(e))
        else:
            # CEK PAID STATUS
            # if paid then send activate service iot
            return response(200, data=payments_data['data'])