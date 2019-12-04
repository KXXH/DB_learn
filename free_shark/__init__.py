import os

from flask_bootstrap import Bootstrap
from flask import (Blueprint,flash,g,render_template,request,session,redirect,url_for,render_template_string,current_app,Flask)
from free_shark.entity.Page import Page
from free_shark.util.json_help import make_json
from flask_login import LoginManager
from flask_uploads import UploadSet, IMAGES, configure_uploads, ALL
try:
    from models import user
except ModuleNotFoundError:
    from .models import user

from flask_sqlalchemy import SQLAlchemy

try:
    import auth
except ModuleNotFoundError:
    from . import auth

try:
    import comController
except ModuleNotFoundError:
    from . import comController

path = os.path.split(os.path.abspath(__file__))[0]
UPLOAD_FOLDER = path + "\\static\\image"

def create_app(test_config=None):
    app=Flask(__name__)
    app.config.from_pyfile('free_shark.cfg')
    app.config.from_pyfile('db_config.cfg')
    app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER
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

    try:
        import db
    except ModuleNotFoundError:
        from . import db
    db.init_app(app)
    
    app.register_blueprint(auth.bp)
    app.register_blueprint(comController.bp)

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
        from db import get_db
        test_db=get_db()
        print(test_db)
        return "aaa"

    @app.route('/test')
    def test_path():
        return path

    return app

if __name__=="__main__":
    app=create_app()
    app.run()
