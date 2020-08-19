
from flask_restful import Resource,reqparse
from flask_jwt_extended import (jwt_required,get_jwt_claims,
                                jwt_optional,get_jwt_identity,
                                fresh_jwt_required
                                )
from models.item import ItemModel

class Item(Resource):
    parser = reqparse.RequestParser()
    parser.add_argument('price',
                        type=float,
                        required=True,
                        help="this field cannot be left blank!"
                        )
    parser.add_argument('store_id',
                        type=int,
                        required=True,
                        help="Store id is needed"
                        )

    @jwt_required
    def get(self,name):
        item=ItemModel.find_by_item_name(name)
        if item:
            return item.json()
        return {"message":"Item not found"},404

    @fresh_jwt_required
    def post(self,name):
        if ItemModel.find_by_item_name(name):
            return {'Message':"Item with name: '{}' already exits".format(name)},400
        request_data = Item.parser.parse_args()
        item=ItemModel(name,**request_data)
        res=item.saveItem()
        if res:

            return item.json(),201
        else:
            return {"message":"Error occured while saving the item!"},401

    @jwt_required
    def delete(self,name):
        claims=get_jwt_claims()
        if not claims['is_admin']:
            return {"message":"Admin privilege required"},401
        item=ItemModel.find_by_item_name(name)
        if item:
            item.delete_from_db()
            return {'message':'Item deleted'},201
        else:
            return {"message":f"{name} is not available"},401

    def put(self,name):

        data=Item.parser.parse_args()

        item=ItemModel.find_by_item_name(name)

        if item:

            item.set_price(data['price'])
        else:
            item = ItemModel(name,data['price'],data['store_id'])
        try:
            item.saveItem()
            return item.json()
        except:
            return {"message": "Error occured while saving the Item to db"}, 500




class ItemList(Resource):
    @jwt_optional
    def get(self):
        user_id=get_jwt_identity()
        items=[item.json() for item in  ItemModel.find_all()]
        if user_id:
            return {"items": items}, 200
        return {"Items":[item['name'] for item in items],
                "message":"Log in to get more data"
                }, 200



