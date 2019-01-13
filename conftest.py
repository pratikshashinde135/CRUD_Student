import pytest
import flask
from flask_sqlalchemy import SQLAlchemy
import app
from app import DB as _db


@pytest.fixture(scope='session')
def test_resp_code_db():
    test_app = app.APP
    client = test_app.test_client()
    app.DB.create_all()
    yield client
    app.DB.drop_all()


@pytest.fixture(scope="session")
def test_resp_code():
    test_app = app.APP
    client = test_app.test_client()
    return client
