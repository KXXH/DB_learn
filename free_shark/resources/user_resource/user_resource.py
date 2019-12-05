from flask import abort,current_app
from flask_restful import Resource,reqparse,fields, marshal_with
from flask_principal import Permission,RoleNeed,UserNeed
from free_shark.models.user import User
from free_shark.exceptions.user_model_exception import UsernameDuplicate,UserNotFound
from flask_login import login_required,current_user
from free_shark.utils import admin_login_required,drop_value_from_request
from free_shark.resources.configs import Base_Response_Fields,User_Search_Fields

class UserUpdatePermission(Permission):
    def __init__(self,user_id):
        super().__init__()
        self.needs=set([RoleNeed("admin"),UserNeed(user_id)])  #only user himself and admin can edit


class UserDeletionPermission(Permission):
    def __init__(self,user_id):
        super().__init__(RoleNeed("admin"))
        self.excludes=set([UserNeed(user_id)])  #用户不能删除用户自身



class UserResourceAdd(Resource):
    """增加用户"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username",required=True)
        self.parser.add_argument("password",required=True)
        self.parser.add_argument("email",required=True)
        pass

    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        user=User.create_user(**d)
        return Base_Response_Fields("success!")

    def get(self):
        return self.post()

        


class UserResourceSearch(Resource):
    """搜索用户"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("username",required=False)    #精准查询的行
        self.parser.add_argument("email",required=False)  #精准查询的内容
        self.parser.add_argument("page_num",required=True,type=int)
        self.parser.add_argument("page_size",required=True,type=int)
    
    @drop_value_from_request()
    @admin_login_required
    @marshal_with(User_Search_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        print(d)
        users,count=User.search_user(**d)
        return User_Search_Fields(users,count)

    def get(self):
        return self.post()


class UserResourceDelete(Resource):
    """删除用户"""

    def __init__(self):
        self.parser = reqparse.RequestParser()
        self.parser.add_argument("id",required=True,type=int)

    @admin_login_required
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        d=self.parser.parse_args()
        id=d['id']
        permission=UserDeletionPermission(id)
        if not permission.can():
            abort(401)
        user=User.get_user_by_id(id)
        if user is None:
            raise UserNotFound("id",id)
        else:
            user.delete_user()
            return Base_Response_Fields("success")

    def get(self):
        return self.post()


class UserResourceUpdate(Resource):
    """修改用户"""

    def __init__(self):
        self.parser=reqparse.RequestParser()
        self.parser.add_argument("id",required=True,type=int)
        self.parser.add_argument("username",required=False)
        self.parser.add_argument("password",required=False)
        self.parser.add_argument("email",required=False)
    
    @marshal_with(Base_Response_Fields().resource_fields)
    def post(self):
        
        d=self.parser.parse_args()
        id=d['id']
        permission=UserUpdatePermission(id)
        if not permission.can():
            abort(401)
        user=User.get_user_by_id(id)
        if user is None:
            raise UserNotFound("id",id)
        if d.get("username",None) is not None:
            user.username=d.get("username",None)
        if d.get("password",None) is not None:
            user.password=d.get("password","")
        if d.get("email",None) is not None:
            user.email=d.get("email",None)
        
        if id==current_user.id:
            current_app.login_manager.reload_user(user)

        return Base_Response_Fields("success!")

    def get(self):
        return self.post()
