from flask_restful import Resource
from models.store import StoreModel

class Stores(Resource):

    def get(self,name):
        store=StoreModel.find_by_store_name(name)
        if store:
            return store.json()
        return {"message":"Store not found"},404


    def post(self,name):

        if StoreModel.find_by_store_name(name):
            return {"message": f"Store with name : {name} already exists !"}, 400
        store=StoreModel(name)
        try:
            store.save_to_db()
        except e:
            return {"message":e},500
        return store.json()

    def delete(self,name):
        store=StoreModel.find_by_store_name(name)
        if store:
            try:
                store.delete_from_db()
                return {"message":"Store deleted"}
            except e:
                return {"message":e},500
        return {"message":"Store doesn't exist !"}


class StoreList(Resource):
    def get(self):
        return {"Stores":[store.json() for store in  StoreModel.find_all()]}

