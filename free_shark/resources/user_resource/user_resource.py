from flask_restful import Resource,reqparse,fields, marshal_with
from free_shark.models.user import User
from free_shark.exceptions.user_model_exception import UsernameDuplicate
from flask_login import login_required
from free_shark.utils import admin_login_required,with_default_val,format_query_dict
from free_shark.resources.configs import Base_Response_Fields,User_Field,User_Search_Fields


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

    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields, envelope='resource')
    def get(self):
        d=self.parser.parse_args()
        user=User.create_user(**d)

        return Base_Response_Fields("success!")

        
class UserResourceSearch(Resource):
    parser = reqparse.RequestParser()

    def __init__(self):
        self.parser.add_argument("username",required=True,type=with_default_val(default_val="%%"))    #精准查询的行
        self.parser.add_argument("email",required=False,type=with_default_val(default_val="%%"))  #精准查询的内容
        self.parser.add_argument("page_num",required=True,type=int)
        self.parser.add_argument("page_size",required=True,type=int)
    
    @admin_login_required
    @marshal_with(User_Search_Fields().resource_fields, envelope='resource')
    def post(self):
        d=self.parser.parse_args()
        users=User.search_user(**d)
        return User_Search_Fields()

    @format_query_dict("%%")
    @admin_login_required
    @marshal_with(User_Search_Fields().resource_fields, envelope='resource')
    def get(self):
        d=self.parser.parse_args()
        print(d)
        users=User.search_user(**d)
        return User_Search_Fields()
