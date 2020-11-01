from flask_restful import Resource, reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from blacklist import BLACKLIST

from flask_jwt_extended import  (
    create_access_token, 
    create_refresh_token, 
    jwt_refresh_token_required,
    get_jwt_identity,
    jwt_required,
    get_raw_jwt
    )

_user_parser = reqparse.RequestParser()
_user_parser.add_argument('username', 
                          type=str, 
                          required=True, 
                          help="this field cannot be left blank")
_user_parser.add_argument('password', 
                           type=str, 
                           required=True, 
                           help="this field cannot be left blank")


class UserRegister(Resource):
    def post(self):
        data = _user_parser.parse_args()

        if UserModel.find_by_username(data['username']):
            return {"message": "A user with that username already exists"}, 400

        user = UserModel(**data)
        user.save_to_db()
        return {'message': 'user created successfully'}, 201


class User(Resource):

    @classmethod
    def get(cls,user_id):
        user= UserModel.find_by_userid(user_id)
        if not user:
            return {'message':'user not found'}, 404
        return user.json()

    @classmethod
    def delete(cls, user_id):
        user = UserModel.find_by_userid(user_id)
        if not user:
            return {'message':'user not found'}, 404
        user.delete_from_db()
        return {'message','user is deleted'}, 200


class UserLogin(Resource):

    @classmethod
    def post(cls):
        data = _user_parser.parse_args()

        user = UserModel.find_by_username(data['username'])
        #authenticate
        if user and safe_str_cmp(user.password, data['password']):
            #identity
            access_token= create_access_token(identity=user.id, fresh= True)
            refresh_token= create_refresh_token(user.id)
            return {'access_token':access_token,
                    'refresh_token': refresh_token   
                    }, 200
        return {'message':'Invalid credentials'}, 401


class UserLogout(Resource):
    @jwt_required
    def post(self):
        #current_user = get_jwt_identity()
        # jwt ID , unique identifier for a JWT
        jti = get_raw_jwt()['jti']
        BLACKLIST.add(jti)
        return {'message':'Successfully logged out'}, 200



class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token= create_access_token(identity=current_user, fresh= False)# define your fresh tokens
        return {'access_token': new_token}
