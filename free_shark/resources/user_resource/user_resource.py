from flask_restful import Resource,reqparse,fields, marshal_with
from free_shark.models.user import User
from free_shark.exceptions.user_model_exception import UsernameDuplicate,UserNotFound
from flask_login import login_required
from free_shark.utils import admin_login_required,drop_value_from_request
from free_shark.resources.configs import Base_Response_Fields,User_Search_Fields


class UserResourceAdd(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("username",required=True)
        self.parser.add_argument("password",required=True)
        self.parser.add_argument("email",required=True)
        pass

    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields, envelope='resource')
    def post(self):
        d=self.parser.parse_args()
        user=User.create_user(**d)
        return Base_Response_Fields("success!")

    def get(self):
        return self.post()

        


class UserResourceSearch(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("username",required=True)    #精准查询的行
        self.parser.add_argument("email",required=False)  #精准查询的内容
        self.parser.add_argument("page_num",required=True,type=int)
        self.parser.add_argument("page_size",required=True,type=int)
    
    @drop_value_from_request()
    @admin_login_required
    @marshal_with(User_Search_Fields().resource_fields, envelope='resource')
    def post(self):
        d=self.parser.parse_args()
        users,count=User.search_user(**d)
        return User_Search_Fields(users,count)

    def get(self):
        return self.post()


class UserResourceDelete(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("id",required=True)

    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields,envelope='resource')
    def post(self):
        d=self.parser.parse_args()
        id=d['id']
        user=User.get_user_by_id(id)
        if user is None:
            raise UserNotFound("id",id)
        else:
            user.delete_user()
            return Base_Response_Fields("success")

    def get(self):
        return self.post()


class UserResourceUpdate(Resource):
    parser=reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("id",required=True)
        self.parser.add_argument("username",required=False)
        self.parser.add_argument("password",required=False)
        self.parser.add_argument("email",required=False)
    
    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields,envelope='resource')
    def post(self):
        d=self.parser.parse_args()
        id=d['id']
        user=User.get_user_by_id(id)
        if user is None:
            raise UserNotFound("id",id)
        if d.get("username",None) is not None:
            user.username=d.get("username",None)
        if d.get("password",None) is not None:
            user.password=d.get("password","")
        if d.get("email",None) is not None:
            user.email=d.get("email",None)
        return Base_Response_Fields("success!")

    def get(self):
        return self.post()
        