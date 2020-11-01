from flask import Flask,jsonify
from flask_restful import Api, Resource
from flask_jwt_extended import JWTManager
from db import db

from resources.user import User, UserRegister, UserLogin, UserLogout, TokenRefresh
from resources.item import Item, ItemList
from resources.store import Store, StoreList
from blacklist import BLACKLIST

# model - internal representation, helper
# resource- external representation for clients ..API interaction

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQL_ALCHEMY_MODIFICATIONS'] = False
app.config['PROPAGATE_EXCEPTIONS'] = True
app.secret_key = 'saroj123' 
app.config['JWT_SECRET_KEY']= 'saroj456' #optional if we want both same of diff
app.config['JWT_BLACKLIST_ENABLED']=True
app.config['JWT_BLACKLIST_TOKEN_CHECKS'] =['access','refresh'] #revoke user tokens mandatory
api = Api(app)


@app.before_first_request
def create_table():
    db.create_all()

jwt = JWTManager(app) # not a /auth endpoint

@jwt.user_claims_loader
def add_claims_to_jwt(identity):
    if identity ==1:# will read from config or database rather , to some other system or  API
        return {'is_admin':True}
    return {'is_admin': False}

@jwt.token_in_blacklist_loader
def check_if_token_in_blacklist(decrypted_token):
    return decrypted_token['jti'] in BLACKLIST



@jwt.expired_token_loader #if token expired , then call below to user
def expired_token_callback():
    return jsonify({
        'description':'token expired, please relogin',
        'error': 'token_expired'
    }), 401

@jwt.invalid_token_loader
def invalid_token_callback(error):
        return jsonify({
        'description':'signature verification failed', 
        'error': 'invalid_token'
    }),401


@jwt.unauthorized_loader
def unauthorized_token_callback(error):
        return jsonify({
        'description':'Not authorized, does not contain access token', 
        'error': 'unathorized_token'
    }),401

@jwt.needs_fresh_token_loader
def missing_token_callback(error):
        return jsonify({
        'description':'refresh token not present , refresh your page ', 
        'error': 'invalid_token'
    }),401

@jwt.revoked_token_loader
def revoked_token_callback():# add to revoked token list
        return jsonify({
        'description':'Token has been revokend ,logged out', 
        'error': 'token_revoked'
    }),401



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
api.add_resource(UserLogout,'/logout')
api.add_resource(TokenRefresh,'/refresh')


if __name__ =="__main__":
    db.init_app(app)
    app.run(port=5000, debug=True)