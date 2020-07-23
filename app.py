from flask import Flask, request
from flask_restful import Resource, Api

app = Flask(__name__)
api = Api(app)

items = []

class Items(Resource):
    def get(self, name):
        #for item in items:
            #if item['name'] == name:
             #   return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item': None}, 404
        return {'item': item}, 200 if item else 404

    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)
        if item:
            return {"message": "An Item with name '{}' already exists.".format(name)}, 400

        data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

class ItemList(Resource):
    def get(self):
        return {'item': items}

api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)