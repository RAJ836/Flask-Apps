from blacklist import BLACKLIST
from flask_restful import Resource,reqparse
from models.user import UserModel
from werkzeug.security import safe_str_cmp
from flask_jwt_extended import (create_access_token,
                                create_refresh_token,jwt_refresh_token_required,
                                get_jwt_identity,jwt_required,get_jwt_claims,
                                get_raw_jwt
                                )


_user_parser=reqparse.RequestParser()
_user_parser.add_argument('username',
                              type=str,
                              required=True,
                              help="This field cannot be blank"
                              )
_user_parser.add_argument('password',
                              type=str,
                              required=True,
                              help="This field cannot be blank"
                              )

class UserRegister(Resource):

    def post(self):
        data = _user_parser.parse_args()
        if UserModel.find_by_username(data['username']):
            return {"message":f"User with username: {data['username']} already Exists !"},400
        user = UserModel(**data)
        user.save_to_db()

        return {"message":f"{data['username']} is created !"}


class User(Resource):

    @classmethod
    def get(cls,user_id):
        user = UserModel.find_by_id(user_id)
        if user:
            return user.json()
        else:
            return {"message":"user not found"}, 404

    @classmethod
    @jwt_required
    def delete(cls,user_id):
        claims = get_jwt_claims()
        if not claims['is_admin']:
            return {"message": "Admin privilege required"}, 401
        user=UserModel.find_by_id(user_id)
        try:
            if user:
                return user.delete_from_db()

            else:
                return {"message":"user not found"} , 404
        except:
            return {"message":"Error occured "}


class UserLogin(Resource):

    @classmethod
    def post(cls):

        # get data from parser
        data =_user_parser.parse_args()
        # find user in database
        user = UserModel.find_by_username(data['username'])

        # check password
        if user and safe_str_cmp(user.password,data['password']):
            access_token=create_access_token(identity=user.id,fresh=True)
            refresh_token = create_refresh_token(user.id)
            return {
                "access_token":access_token,
                "refresh_token":refresh_token
            }, 200
        return {"message":"invalid credentials"}, 401


class TokenRefresh(Resource):
    @jwt_refresh_token_required
    def post(self):
        current_user = get_jwt_identity()
        new_token = create_access_token(identity=current_user,fresh=False)
        return {"access_token":new_token}


class UserList(Resource):
    @jwt_required
    def get(self):
        claims=get_jwt_claims()
        if claims['is_admin']:
            users=UserModel.find_all_users()
            return {"users":[user.json() for user in users]}
        return {"message": "Admin privileges are required to access the user information"}

class UserLogout(Resource):
    @jwt_required
    def post(self):
        current_user = UserModel.find_by_id(get_jwt_identity())
        jti = get_raw_jwt()['jti']   # jti is "JWT ID", a unique identifier for a JWT
        BLACKLIST.add(jti)
        return {"message":f"{current_user.username} has been logged out successfully !"}