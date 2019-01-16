import pytest
import app
import flask
from app import *
import unittest
from flask.testing import FlaskClient

# Connection to the database
APP = Flask(__name__)
APP.config["SQLALCHEMY_DATABASE_URI"] = 'mysql://root:pratiksha@localhost/entity'
APP.config['SECRET_KEY'] = "secret"
DB = SQLAlchemy(APP)


@pytest.fixture(scope='module')
def test_resp_code():
    client = app.APP.test_client()
    return client


dict_signup = {
    "username": "omkar",
    "email": "p@gmail.com",
    "password": "omkar"
}
dict_login = {
    "username": "pratiksha",
    "password": "pratiksha"
}
dict_new_class = {
    "class_id": 4,
    "class_name": "B"
}
dict_new_student = {
    "student_id": 1,
    "name": "harsh",
    "class_id": 1,
    "c_leader": "no",
}
dict_new_student2 = {
    "student_id": 2,
    "name": "shree",
    "class_id": 1,
    "c_leader": "yes",
}
dict_update = {
    "studentId": 5,
    "new_name": "rahul",
    "class_id": 1
}

dict_update2 = {
    "studentId": 6,
    "new_name": "Prabha",
    "class_id": 2
}

dict_delete = {
    "id": 5
}


def test_new_student(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_student', data=dict_new_student)
    assert resp.status_code == 200


def test_add_student(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/add_new_student', data=dict_new_student)
    assert resp.status_code == 200


def test_new_student2(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_student', data=dict_new_student2)
    assert resp.status_code == 200


def test_add_student2(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/add_new_student', data=dict_new_student2)
    assert resp.status_code == 200


def test_new_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/new_class', data=dict_new_class)
    assert resp.status_code == 200


def test_add_class(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/adding_class', data=dict_new_class)
    assert resp.status_code == 200


def test_update_rec(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_data', data=dict_update)
    assert resp.status_code == 200


def test_update(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update', data=dict_update)
    assert resp.status_code == 302


def test_update_rec2(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/update_data', data=dict_update2)
    assert resp.status_code == 200


def test_delete(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/delete', data=dict_delete)
    assert resp.status_code == 302


def test_class_table(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="pratiksha"')
    assert resp.status_code == 200


def test_student_show(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/show_all?name="pratiksha"')
    assert resp.status_code == 302


def test_user_id(test_resp_code):
    abc = test_resp_code
    resp = abc.post('/?name="pratiksha"')
    assert resp.status_code == 200


def test_signup(test_resp_code):
    xyz = test_resp_code
    resp = xyz.post('/signup', data=dict_signup)
    assert resp.status_code == 200


def test_login(test_resp_code):
    xyz = test_resp_code
    resp = xyz.post('/login', data=dict_login)
    assert resp.status_code == 200



