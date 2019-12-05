from flask import Flask
import pytest
import free_shark
@pytest.fixture
def app():
    app = free_shark.create_app()
    app.config.from_pyfile('free_shark.cfg')
    app.config.from_pyfile('db_config.cfg')
    app.config['WTF_CSRF_ENABLED'] = False
    with app.app_context():
        free_shark.db.init_db()
    yield app

@pytest.fixture
def client(app):
    with app.test_client() as client:
        with app.app_context():
            free_shark.db.init_db()
        yield client
