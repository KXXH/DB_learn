from flask import Flask
import pytest
import free_shark
@pytest.fixture
def app():
    app = Flask(__name__)
    app.config.from_pyfile('free_shark.cfg')
    app.config.from_pyfile('db_config.cfg')
    with app.app_context():
        free_shark.db.init_db()
    yield app