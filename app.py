# Create proper REST API with principals

from flask import Flask
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

# Each resource must be a class that inherits from Resource
class Item(Resource):
    def get(self, name):
        for item in items:
            if item['name'] == name:
                return(item)

        return({'item': None}), 404 # stat code for NOT FOUND

    def post(self, name):
        item = {'name': name, 'age': 1000}
        items.append(item)
        return(item), 201 # stat code for CREATED

api.add_resource(Item, '/item/<string:name>')

app.run(port=5000)
