import os

from flask_bootstrap import Bootstrap
from flask import Flask,render_template,request
from flask_login import LoginManager
from free_shark.models.commodity import Commodity
from free_shark.entity.Page import Page
import sys

try:
    from models import user
except ModuleNotFoundError:
    from .models import user

from flask_sqlalchemy import SQLAlchemy

try:
    import auth
except ModuleNotFoundError:
    from . import auth


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

    try:
        import db
    except ModuleNotFoundError:
        from . import db
    db.init_app(app)
    
    app.register_blueprint(auth.bp)

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

    @app.route('/hello',methods=("POST","GET"))
    def hello():
        if request.method == 'GET':
            current = request.args.get('current') or 1
            current = int(current)
            commodity_name = request.args.get('commodity_name') or None
            commodity_type = request.args.get('commodity_type') or None
            print(commodity_name)
            print(commodity_type)
            r = Commodity.search_commodity(-1,0,sys.maxsize,1,commodity_type,commodity_name)
            # 设置分页
            page = Page()
            page.current = current
            page.rows = r
            page.path = '/hello'
            offset = page.get_offset()
            coms = Commodity.search_commodity(-1,offset,page.limit,0,commodity_type,commodity_name)
            return render_template("commodity.html", commodities=coms,page=page)

    return app

if __name__=="__main__":
    app=create_app()
    app.run()


    
