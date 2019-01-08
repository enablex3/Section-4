# Create proper REST API with principals

from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required
from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'philly_beans'
api = Api(app)

jwt = JWT(app, authenticate, identity) # /auth

items = []

# Each resource must be a class that inherits from Resource
class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('age', 
        type=int, 
        required=True, 
        help='This field cannot be blank!'
    )
    @jwt_required() # authenticate before request can be made
    def get(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        return({'item': item}), 200 if item else 404

    def post(self, name):
        if next(filter(lambda x: x['name'] == name, items), None) is not None:
            return({'message': '{} already exists.'.format(name)}), 400
        
        data = Item.parser.parse_args()
        age = data['age']
        item = {'name': name, 'age': age}
        items.append(item)
        return({'message': '{} has been added'.format(name)}, item), 201 # stat code for CREATED

    def delete(self, name):
        global items # call existing items list
        item =  next(filter(lambda x: x['name'] == name, items), None)
        if item:
            item_idx = items.index(item)
            del(items[item_idx])
            return({'message': '{} deleted.'.format(name)}), 200 if item else 400
        else:
            return({'message': '{} does not exist.'.format(name)})

    def put(self, name):
        data = parser.parse_args()
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item is None:
            age = data['age']
            item = {'name': name, 'age': age}
            items.append(item)
            return({'message': '{} has been added'.format(name)}, item), 201
        else:
            item_idx = items.index(item)
            item.update(data)
            items[item_idx] = item 
            return({'message': '{} has been updated'.format(name)}, item), 200

class ItemList(Resource):
    def get(self):
        return({'items': items})

api.add_resource(Item, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000)
