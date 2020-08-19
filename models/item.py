from db import db
from models.store import StoreModel

class ItemModel(db.Model):
    __tablename__ = "items"

    id = db.Column(db.Integer , primary_key=True)
    name = db.Column(db.String(80))
    price = db.Column(db.Float(precision=2))

    store_id =db.Column(db.Integer,db.ForeignKey('stores.id'))
    store=db.relationship('StoreModel')

    def __init__(self,name,price,store_id):
        self.name=name
        self.price=price
        self.store_id=store_id

    def set_price(self,price):
        self.price=price

    def set_name(self,name):
        self.name=name

    def json(self):
        return {
            "id":self.id,
            'name':self.name,
            'price':self.price,
            "store_id":self.store_id
        }

    @classmethod
    def find_by_item_name(cls,name):
        return cls.query.filter_by(name=name).first()

    @classmethod
    def find_all(cls):
        return cls.query.all()

    def saveItem(self):

        try:

            db.session.add(self)
            db.session.commit()
            res = True
        except:
            res = False
        return res


    def delete_from_db(self):

        try:
            db.session.delete(self)
            db.session.commit()
            res = True
        except:
            res = False
        return res