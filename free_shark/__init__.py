import os

from flask import Flask
from flask_bootstrap import Bootstrap
from flask_login import LoginManager

import auth

from models import user

def create_app(test_config=None):
    app=Flask(__name__)
    app.config.from_mapping(
        SECRET_KEY='dev',
        DATABASE=os.path.join(app.instance_path, 'free_shark.sqlite'),
    )
    app.config.from_pyfile('free_shark.cfg')
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

    app.register_blueprint(auth.bp)

    login_manager=LoginManager()
    
    login_manager.init_app(app)

    bootstrap=Bootstrap()
    bootstrap.init_app(app)
    @login_manager.user_loader
    def load_user(userid):
        if userid=='3':
            return user.User("user","pass")
        else:
            return None

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        return 'Hello, World!'

    return app

if __name__=="__main__":
    app=create_app()
    app.run()