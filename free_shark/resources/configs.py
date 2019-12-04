NOT_FOUND=404
USERNAME_DUPLICATE=409
USER_EMAIL_INVALID=410
SUCCESS=200


errors = {
    'UsernameDuplicate': {
        'message': "该用户名已被占用",
        'status': USERNAME_DUPLICATE
    },
    'UserEmailInvalid': {
        'message': "该邮箱格式不正确",
        'status': USER_EMAIL_INVALID
    },
    'UserNotFound':{
        'message':"用户未找到",
        'status':NOT_FOUND
    }
}

from flask_restful import fields
class Base_Response_Fields:
    
    def __init__(self,message=None,status=SUCCESS):
        self.base_response_fields={
            "status":fields.Integer,
            "message":fields.String
        }
        self.status=status
        self.message=message
    
    @property
    def resource_fields(self):
        return self.base_response_fields.copy()


from free_shark.models.user import User
import json
class User_Search_Fields(Base_Response_Fields):
    def __init__(self,data=None,count=0,**kwargs):
        super().__init__(**kwargs)
        self.user_fields={
            "id":fields.Integer,
            "username":fields.String,
            "email":fields.String,
            "activation":fields.String,
            "type":fields.Integer,
            "status":fields.Integer,
            "create_time":fields.DateTime
        }
        self.data=data
        self.count=count
    
    @property
    def resource_fields(self):
        d=super().resource_fields.copy()
        d['data']=fields.List(fields.Nested(self.user_fields))
        d['count']=fields.Integer
        return d