from free_shark.resources.blue_print import bp
from flask_restful import Api, Resource
from free_shark.resources.user_resource import user_resource
from free_shark.resources.configs import errors


api=Api(bp,errors=errors)
api.add_resource(user_resource.UserResourceAdd,'/user/admin/add')
api.add_resource(user_resource.UserResourceSearch,'/user/admin/search')
api.add_resource(user_resource.UserResourceDelete,'/user/admin/delete')
api.add_resource(user_resource.UserResourceUpdate,'/user/admin/update')