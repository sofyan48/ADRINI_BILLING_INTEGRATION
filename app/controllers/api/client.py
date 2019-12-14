from flask_restful import Resource, reqparse
from app.helper.rest import *
from app.libs import utils
from app.helper.rest import response
from app.models import model as db


class ClientList(Resource):
    def get(self):
        try:
            client_data = utils.get_ninja(api="clients")
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=client_data['data'])

class ClientListById(Resource):
    def get(self, id):
        try:
            client_data = utils.get_ninja(api="clients/"+id)
        except Exception as e:
            return response(401, message=str(e))
        else:
            return response(200, data=client_data['data'])

class ClientListByEmail(Resource):
    def get(self, email):
        try:
            client_data = utils.get_ninja(api="clients")
        except Exception as e:
            return response(401, message=str(e))
        
        data = list()
        for i in client_data['data']:
            if i['contacts'][0]['email'] == email:
                data = i
        
        return response(200, data=data)

        

class CreateClient(Resource):
    def post(self):
        parser = reqparse.RequestParser()
        parser.add_argument('name', type=str, required=True)
        parser.add_argument('vat', type=str, required=True)
        parser.add_argument('id_number', type=str, required=True)
        parser.add_argument('address1', type=str, required=False)
        parser.add_argument('address2', type=str, required=False)
        parser.add_argument('city', type=str, required=False)
        parser.add_argument('state', type=str, required=False)
        parser.add_argument('postal_code', type=str, required=False)
        parser.add_argument('country_id', type=str, required=False)
        parser.add_argument('work_phone', type=str, required=True)
        parser.add_argument('email', type=str, required=True)
        parser.add_argument('first_name', type=str, required=True)
        parser.add_argument('last_name', type=str, required=True)
        args = parser.parse_args()
        client_data = {
            "name": args['name'],
            "vat_number": args['vat'],
            "id_number": args['id_number'],
            "address1": args['address1'],
            "address2": args['address2'],
            "city": args['city'],
            "state": args['state'],
            "postal_code": args['postal_code'],
            "country_id": args['country_id'],
            "work_phone": args['work_phone']
        }
        client_data_temps = utils.post_ninja("clients", client_data)
        contact_data = client_data_temps['data']['contacts']
        contact_db = db.get_by_id("contacts", "public_id", contact_data[0]['id'])[0]
        
        contact_data_update = {
            "where": {
                "id": str(contact_db['id'])
            },
            "data": {
                "email": args['email'],
                "first_name": args['first_name'],
                "last_name": args['last_name'],
                "phone": args['work_phone']
            }
        }
        
        try:
            a = db.update("contacts", contact_data_update)
        except Exception as e:
            return response(401, message=str(e))
        else:
            id = str(client_data_temps['data']['id'])
            client_data = utils.get_ninja(api="clients/"+id)['data']
        return response(200, data=client_data)

