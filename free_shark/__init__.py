import os
from flask import Flask,render_template,request
from flask_bootstrap import Bootstrap
from flask_login import LoginManager,current_user
from flask_restful import Resource, Api
from flask_wtf.csrf import CSRFProtect
from flask_mail import Mail
from flask_principal import Principal, Permission, RoleNeed,identity_loaded,identity_changed,Identity,AnonymousIdentity,UserNeed
from free_shark.models import user
from free_shark import resources
from free_shark import auth,db
from flask_sqlalchemy import SQLAlchemy
from free_shark import comController
from free_shark.utils import admin_login_required,load_config_from_envvar
from free_shark.models.commodity import Commodity
from free_shark.entity.Page import Page
import sys

path = os.path.split(os.path.abspath(__file__))[0]
UPLOAD_FOLDER = path + "\\static\\image"

def create_app(test_config=None):
    app=Flask(__name__)
    try:
        app.config.from_pyfile('free_shark.cfg')
        app.config.from_pyfile('db_config.cfg')
        app.config.from_pyfile('mail_config.cfg')
    except:
        pass
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
    app.config['WTF_CSRF_ENABLED'] = False
    if test_config is None:
    # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    d=load_config_from_envvar()
    app.config.from_mapping(d)
    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(resources.bp)
    app.register_blueprint(comController.bp)
   
    principals = Principal(app)
    principals.init_app(app)

    login_manager=LoginManager()   
    login_manager.init_app(app)

    bootstrap=Bootstrap()
    bootstrap.init_app(app)
  
    csrf=CSRFProtect(app)
    csrf.init_app(app)

    mail = Mail()
    mail.init_app(app)

    
    @login_manager.user_loader
    def load_user(userid):
        try:
            id=int(userid)
            return user.User.get_user_by_id(id)
        except:
            return user.User.get_user_by_token(userid) 



    # a simple page that says hello
    
    @identity_loaded.connect_via(app)
    def on_identity_loaded(sender, identity):
        print("indentity加载完毕!")
        identity.user=current_user
        if current_user is not None and not current_user.is_anonymous:
            identity.provides.add(UserNeed(current_user.id))
            for role in current_user.role:
                identity.provides.add(RoleNeed(role))
        else:
            identity.provides.add(RoleNeed("anonymous"))

    return app

if __name__=="__main__":
    app=create_app()
    app.run()
