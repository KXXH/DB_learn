from functools import wraps
from flask import request,current_app
from flask_login import current_user,login_required

def admin_login_required(func):
    @wraps(func)
    @login_required
    def decorated_view(*args,**kwargs):
        print(current_user.email)
        if not current_user.is_admin:
            print("not login")
            return current_app.login_manager.unauthorized()
        else:
            print("login")
            return func(*args,**kwargs)
    return decorated_view

from flask_restful import fields
class Arg_Default_Val(fields.Raw):
    def __init__(self,default_class=str,default_val=None):
        self.default_val=default_val
        self.default_class=default_class
    
    def __call__(self,value):
        print("__call__")
        print(self.default_val)
        print(value)
        if value is None:
            return self.default_class(self.default_val)
        else:
            return self.default_class(value)

def with_default_val(default_class=str,default_val=None):
    return Arg_Default_Val(default_class,default_val)

def format_query_dict(default):
    def formatter(func):
        @wraps(func)
        def decorated_view(self):
            d=self.parser.parse_args()
            for key in d:
                if d[key] is None:
                    self.parser.remove_argument(key)
            return func(self)
        return decorated_view
    return formatter
