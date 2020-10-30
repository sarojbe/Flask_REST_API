from werkzeug.security import safe_str_cmp
from models.user import UserModel

# curl http://127.0.0.1:5000/auth  -H "Content-Type: application/json" -d "{\"username\":\"bob\",\"password\":\"asof\"}"



def authenticate(username,password):
    user = UserModel.find_by_username(username)
    if user and safe_str_cmp(user.password,password):
        return user

def identity(payload):
    user_id = payload['identity']
    return UserModel.find_by_userid(user_id)
