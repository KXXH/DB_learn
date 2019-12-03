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
class User_Field(fields.Raw):
    def format(self,value):
        print("fprmating")
        if type(value)==User:
            return {
                "username":value.username,
                "email":value.email,
                "activation":value.activation,
                "type":value.type,
                "status":value.type,
                "create_time":value.create_time
            }
        elif type(value)==list:
            ans=[]
            for user in value:
                assert type(user)==User
                ans.append({
                    "username":user.username,
                    "email":user.email,
                    "activation":user.activation,
                    "type":user.type,
                    "status":user.type,
                    "create_time":user.create_time
                })
            return ans

class User_Search_Fields(Base_Response_Fields):
    def __init__(self,*args,**kwargs):
        super().__init__(*args,**kwargs)
    
    @property
    def resource_fields(self):
        d=super().resource_fields.copy()
        d['data']=User_Field()
        return d