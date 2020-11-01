from flask import Flask
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from db import db

from resources.user import User, UserRegister, UserLogin
from resources.item import Item, ItemList
from resources.store import Store, StoreList


# model - internal representation, helper
# resource- external representation for clients ..API interaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQL_ALCHEMY_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'saroj123' 
app.config['JWT_SECRRET_KEY']= 'saroj456' #optional if we want both same of diff
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()

jwt = JWTManager(app) # not a /auth endpoint


class Home(Resource):
    @staticmethod
    def get():
        return "{'message': 'API Landing Page'}"


api.add_resource(Home,'/')
api.add_resource(Item,'/item/<string:name>')
api.add_resource(ItemList,'/items')
api.add_resource(Store,'/store/<string:name>')
api.add_resource(StoreList,'/stores')
api.add_resource(User,'/user/<int:user_id>')
api.add_resource(UserRegister,'/register')
api.add_resource(UserLogin,'/login')


if __name__ =="__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)