import os
from flask import Flask,render_template
from flask_login import LoginManager
import auth
from models import user
from flask_sqlalchemy import SQLAlchemy

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


    db = SQLAlchemy(app)
    class User(db.Model):
        __tablename__ = 'user'
        id = db.Column(db.Integer, primary_key = True)
        username = db.Column(db.String(64),unique=True,index=True)

        def __repr__(self):
                return '<User %r>' % self.username 
    
    app.register_blueprint(auth.bp)

    login_manager=LoginManager()

    login_manager.init_app(app)

    @login_manager.user_loader
    def load_user(userid):
        if userid=='3':
            return user.User("user","pass")
        else:
            return None

    # a simple page that says hello
    @app.route('/hello')
    def hello():
        sql = 'update user set username = "hahah" where id = 1'
        db.session.execute(sql)
        user = User.query.all()
        return render_template('userTest.html',user=user)

    return app

if __name__=="__main__":
    app=create_app()
    app.run()
