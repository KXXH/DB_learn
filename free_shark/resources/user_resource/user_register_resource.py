from flask import abort,current_app
from flask_restful import Resource,reqparse,fields,marshal_with
from flask_principal import Permission,RoleNeed,UserNeed
from flask_shark.models.user import User

class UserRegisterPermission(Permission):
    def __init__(self):
        super().__init__()
        self.excludes=set([RoleNeed("user")])   #不允许已登录用户注册
    
