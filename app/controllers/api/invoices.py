from flask_restful import Resource, reqparse
from app.helper.rest import *
from app.libs import utils
from app.helper.rest import response
from app.models import model as db

def percentage(percent, whole):
    return (percent * whole) / 100


class InvoiceList(Resource):
    def get(self):
        try:
            invoice_data = utils.get_ninja(api="invoices")
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=invoice_data['data'])

class InvoiceListById(Resource):
    def get(self, id):
        try:
            invoice_data = utils.get_ninja(api="invoices/"+id)
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=invoice_data['data'])

class InvoiceCreate(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('client_id', type=str, required=True)
        parser.add_argument('is_recurring', type=str, required=True)
        parser.add_argument('tax_rate1', type=str, required=True)
        parser.add_argument('tax_name1', type=str, required=True)
        parser.add_argument('is_amount_discount', type=str, required=False)
        parser.add_argument('service_type', type=str, required=True)
        parser.add_argument('product_id', type=str, required=True)
        args = parser.parse_args()

        try:
            get_products = utils.get_ninja("products/"+str(args['product_id']))['data']
        except Exception as e:
            print(e)
        tax_value = percentage(get_products['cost'], get_products['tax_rate1'])

        data_insert = {
            "client_id": args['client_id'],
            "is_recurring": args['is_recurring'],
            "tax_rate1": str(args['tax_rate1']),
            "tax_name1": str(args['tax_name1']),
            "is_amount_discount": str(args['is_amount_discount']),
            "custom_value1": args['service_type']
        }
        try:
            invoice_data_temps = utils.post_ninja("invoices", data_insert)['data']
        except Exception as e:
            print(e)
        get_invoice_id = db.get_by_id("invoices","public_id", invoice_data_temps['id'])[0]
        data_insert_items = {
            "account_id": "1",
            "user_id": "1",
            "invoice_id": str(get_invoice_id['id']),
            "product_id": str(args['product_id']),
            "product_key": get_products['product_key'],
            "notes": get_products['notes'],
            "custom_value1": args['service_type'],
            "tax_rate1": "0",
            "tax_name1": "",
            "tax_rate2":"0",
            "tax_name2": "",
            "discount": "0",
            "cost": str(get_products['cost']),
            "public_id": str(invoice_data_temps['id']),
            "qty":"1"
        }

        try:
            db.insert("invoice_items", data_insert_items)
        except Exception as e:
            print(e)
        else:
            invoice_updates = {
                "where":{
                    "public_id": str(invoice_data_temps['id'])
                },
                "data":{
                    "invoice_status_id": "2",
                    "amount": str(get_products['cost']+tax_value),
                    "balance": str(get_products['cost']+tax_value)
                }
            }
            try:
                db.update("invoices", data=invoice_updates)
            except Exception as e:
                print("DISINI",e)
        email_data = {
            "invoice_number":invoice_data_temps['invoice_number']
        }
        try:
            send_email = utils.post_ninja("email_invoice", email_data)
        except Exception as e:
            print(e)
        try:
            get_invoice = utils.get_ninja("invoices/"+str(invoice_data_temps['id']))
        except Exception as e:
            return response(200, message=str(e))
        else:
            return response(200, data=get_invoice)