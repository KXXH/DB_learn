from flask import abort,current_app
from flask_restful import Resource,reqparse,fields,marshal_with
from flask_principal import Permission,RoleNeed,UserNeed
from free_shark.models.user import User
from free_shark.resources.configs import Base_Response_Fields,USER_EMAIL_INVALID,USERNAME_DUPLICATE

class UserRegisterPermission(Permission):
    def __init__(self):
        super().__init__()
        self.excludes=set([RoleNeed("user")])   #不允许已登录用户注册

class UsernameAvailable(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("username",required=True)

    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        user=User.get_user_by_username(d['username'])
        if user is None:
            return Base_Response_Fields("ok")
        else:
            return Base_Response_Fields("该用户名已被注册!",USERNAME_DUPLICATE)

class EmailAvailable(Resource):
    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("email",required=True)
    
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        users=User.search_user_without_page(email=d['email'])
        if len(users)==0:
            return Base_Response_Fields("ok")
        else:
            return Base_Response_Fields("该邮箱已被注册!",USER_EMAIL_INVALID)
