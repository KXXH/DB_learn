import os

from flask_bootstrap import Bootstrap
from flask import Flask,render_template,request
from flask_login import LoginManager
from flask_restful import Resource, Api
from free_shark.models import user
from free_shark import resources
from free_shark import auth,db
from flask_sqlalchemy import SQLAlchemy
from free_shark.utils import admin_login_required


def create_app(test_config=None):
    app=Flask(__name__)
    app.config.from_pyfile('free_shark.cfg')
    app.config.from_pyfile('db_config.cfg')
    if test_config is None:
    # load the instance config, if it exists, when not testing
        app.config.from_pyfile('config.py', silent=True)
    else:
        # load the test config if passed in
        app.config.from_mapping(test_config)

    # ensure the instance folder exists
    try:
        os.makedirs(app.instance_path)
    except OSError:
        pass

    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(resources.bp)
   


    login_manager=LoginManager()   
    login_manager.init_app(app)

    bootstrap=Bootstrap()
    bootstrap.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        return user.User.get_user_by_id(int(userid))

    # a simple page that says hello
    

    @app.route('/db')
    def test_db():
        test_db=db.get_db()
        print(test_db)
        return "aaa"

    
    @app.route('/hello',methods=("POST","GET"))
    @admin_login_required
    def hello():
        return "hello"

    return app

if __name__=="__main__":
    app=create_app()
    app.run()


    
