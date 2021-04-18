from flask_jwt import jwt_required
from flask_restful import Resource, reqparse

from models.item import ItemModel as item_model


class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help='This field is required'
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help='This field is required'
                        )

    @jwt_required()
    def get(self, name):
        item = item_model.find_by_name(name)
        if item:
            return item.json()
        return {'message': 'Item not found'}, 404

    def post(self, name):
        if item_model.find_by_name(name):
            return {'message': f'Item already exists.'}, 403

        data = Item.parser.parse_args()

        item = item_model(name, **data)

        try:
            item.save_to_db()
        except:
            return {'message': 'An error occurred inserting the item'}, 500

        return item.json(), 201

    def delete(self, name):
        item = item_model.find_by_name(name)

        if item:
            item.delete_from_db()
            return {}, 204

        return {'message': 'Item not found'}, 404

    def put(self, name):
        data = Item.parser.parse_args()

        item = item_model.find_by_name(name)

        if item:
            item.price = data['price']
            item.store_id = data['store_id']
        else:
            item = item_model(name, **data)

        item.save_to_db()

        return item.json()


class ItemList(Resource):
    def get(self):
        return {'items': [item.json() for item in item_model.query.all()]}
