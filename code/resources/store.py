from flask_restful import Resource

from models.store import StoreModel as store_model


class Store(Resource):
    def get(self, name):
        store = store_model.find_by_name(name)

        if store:
            return store.json()

        return {'message': 'Store not found'}, 404

    def post(self, name):
        if store_model.find_by_name(name):
            return {'message': f'Store {name} already exists'}, 403

        store = store_model(name)

        try:
            store.save_to_db()
        except:
            return {'message': 'An error occurred while creating the store'}, 500

        return store.json(), 201

    def delete(self, name):
        store = store_model.find_by_name(name)

        if store:
            store.delete_from_db()
            return {}, 204

        return {'message': f'Store {name} cannot be found'}, 404


class StoreList(Resource):
    def get(self):
        return {'stores': [store.json() for store in store_model.query.all()]}
