import sys
import os
sys.path.append(os.path.abspath('.'))
import pytest
from free_shark import models
from flask import Flask

@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_pyfile('free_shark.cfg')
    app.config.from_pyfile('db_config.cfg')

    yield app


class TestUser:

    def test_add_user1(self,app):
        with app.app_context():
            user=models.user.User.create_user(username='zjm',password='kxxh',salt='kxxh',email='test@test',activation='act',type=1,status=1)
            assert user is not None
            user=models.user.User.get_user_by_username('zjm')
            assert user is not None
            assert user.password=='kxxh'

    def test_select2(self,app):
        with app.app_context():
            user=models.user.User.get_user_by_id(1)
            assert user is None

    def test_select1(self,app):
        with app.app_context():
            user=models.user.User.get_user_by_id(2)
            assert user is not None

    def test_modify_username1(self,app):
        with app.app_context():
            user=models.user.User.get_user_by_id(3)
            user.username='fcc'
            user=models.user.User.get_user_by_id(3)
            assert user.username=='fcc'