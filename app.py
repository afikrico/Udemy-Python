from flask import Flask, request
from flask_restful import Resource, Api, reqparse
from flask_jwt import JWT, jwt_required

from security import authenticate, identity

app = Flask(__name__)
app.secret_key = 'jose'
api = Api(app)

jwt = JWT(app, authenticate, identity)  #/auth

items = []

class Items(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
        type=float,
        required=True,
        help='This field cannot be left blank!'
    )

    @jwt_required()
    def get(self, name):
        #for item in items:
            #if item['name'] == name:
             #   return item
        item = next(filter(lambda x: x['name'] == name, items), None)
        #return {'item': None}, 404
        return {'item': item}, 200 if item else 404

    @jwt_required()
    def post(self, name):
        item = next(filter(lambda x: x['name'] == name, items), None)

        if item:
            return {"message": "An Item with name '{}' already exists.".format(name)}, 400

        data = Item.parser.parse_args()
        #data = request.get_json()
        item = {'name': name, 'price': data['price']}
        items.append(item)
        return item, 201

    def delete(self, name):
        global items
        items = list(filter(lambda x:x['name'] != name, items), None)
        return {'message': 'Item deleted'}

    def put(self, name):
        data = Item.parser.parse_args() #request.get_json()
        item = next(filter(lambda x:x['name'] == name, items), None)
        if item:
            item.update(data)
        else:
            item = {'name':name, 'price':data['price']}
        
        items.append(item)
        return item

class ItemList(Resource):
    def get(self):
        return {'item': items}

api.add_resource(Items, '/item/<string:name>')
api.add_resource(ItemList, '/items')

app.run(port=5000, debug=True)