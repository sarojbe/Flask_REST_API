from flask import Flask
from flask_restful import Api, Resource
from flask_jwt import JWT

from security import authenticate, identity
from resources.user import UserRegister
from resources.item import Item, ItemList
from resources.store import Store, StoreList



# model - internal representation, helper
# resource- external representation for clients ..API interaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQL_ALCHEMY_MODIFICATIONS'] = False
# app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'saroj'
api = Api(app)



@app.before_first_request
def create_table():
    db.create_all()

jwt = JWT(app, authenticate, identity) # creates a /auth endpoint


class Home(Resource):
    @staticmethod
    def get():
        return "{'message': 'API Landing Page'}"


api.add_resource(Home,'/')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')

api.add_resource(UserRegister,'/register')

if __name__ =="__main__":
    from db import db
    db.init_app(app)
    app.run(port=5000, debug=True)