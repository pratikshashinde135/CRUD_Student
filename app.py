"""
This is main python file for student portal.
It has all the functions to perform CRUD operations on student and class entity.
"""
import time
import datetime
from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required
import pymysql

pymysql.install_as_MySQLdb()

APP = Flask(__name__)
APP.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
APP.config['SECRET_KEY'] = 'secret'
APP.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pratiksha@localhost/entity'
BOOTSTRAP = Bootstrap(APP)
DB = SQLAlchemy(APP)
LOGIN_MANAGER = LoginManager()
LOGIN_MANAGER.init_app(APP)
LOGIN_MANAGER.login_view = 'login'


class User(UserMixin, DB.Model):
    """
    User class to create user table.
    """
    id = DB.Column(DB.Integer, primary_key=True)
    username = DB.Column(DB.String(15), unique=True)
    email = DB.Column(DB.String(50), unique=True)
    password = DB.Column(DB.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password


@LOGIN_MANAGER.user_loader
def load_user(user_id):
    """
    Function to get user id
    """
    return User.query.get(int(user_id))


class LoginForm(FlaskForm):
    """To get data from login form"""
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


class RegisterForm(FlaskForm):
    """To get data from login form"""
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(),
                                             Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    DB.create_all()


@APP.route('/', methods=['GET', 'POST'])
def index():
    """Function for home page"""
    return render_template('index.html')


@APP.route('/login', methods=['GET', 'POST'])
def login():
    """To perform login operation"""
    form = LoginForm()

    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if check_password_hash(user.password, form.password.data):
                login_user(user, remember=form.remember.data)
                return redirect(url_for('show_all'))

        return '<h1>Invalid username or password</h1>'
        # return '<h1>' + form.username.data + ' ' + form.password.data + '</h1>'
    return render_template('login.html', form=form)


@APP.route('/signup', methods=['GET', 'POST'])
def signup():
    """To perform signup operation"""
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data,
                        password=hashed_password)
        DB.session.add(new_user)
        DB.session.commit()

        return '<h1>New user has been created!</h1>'
    return render_template('signup.html', form=form)


class Student(DB.Model):
    """class to create student table"""
    student_id = DB.Column('id', DB.Integer, primary_key=True)
    name = DB.Column(DB.String(100), nullable=False)
    class_id = DB.Column(DB.Integer, DB.ForeignKey('class.c_id'))
    created_on = DB.Column(DB.String(50))
    updated_on = DB.Column(DB.String(50))
    # clas = db.relationship('Class', backref='student', lazy=True)

    def __init__(self, student_id, name, class_id, created_on, updated_on):
        self.student_id = student_id
        self.name = name
        self.class_id = class_id
        self.created_on = created_on
        self.updated_on = updated_on


class Class(DB.Model):
    """class to create class table"""
    c_id = DB.Column(DB.Integer, primary_key=True)
    c_name = DB.Column(DB.String(100), nullable=False)
    c_leader = DB.Column(DB.Integer, DB.ForeignKey('student.id'))
    created_on = DB.Column(DB.String(50))
    updated_on = DB.Column(DB.String(50))
    # students = db.relationship('Student', backref='class', lazy=True)

    def __init__(self, c_id, c_name, c_leader, created_on, updated_on):
        self.c_id = c_id
        self.c_name = c_name
        self.c_leader = c_leader
        self.created_on = created_on
        self.updated_on = updated_on


@APP.route('/show_all', methods=['POST', 'GET'])
@login_required
def show_all():
    """function to display all student's data"""
    return render_template('show_all.html', student=Student.query.all())


@APP.route('/adding_class', methods=['POST'])
def new_class():
    """Function to create new class"""
    if request.method == 'POST':
        print("Inside POST")
        try:
            class_id = request.form.get("class_id")
            class_name = request.form.get("class_name")
            time_stamp = time.time()
            timestamp = datetime.datetime.fromtimestamp(time_stamp)
            date_add = timestamp
            cls = Class(c_id=class_id, c_name=class_name, c_leader=None,
                        created_on=date_add, updated_on=date_add)
            DB.session.add(cls)
            DB.session.commit()
            return '<h1>New class has been created!</h1>'
        except IOError:
            msg = "Error while adding new class"
            print(msg)
            return '<h1>Error while adding new class</h1>'
    return render_template('show_all.html', student=Student.query.all())


@APP.route("/new_class", methods=["GET", "POST"])
def add_class():
    """To add new class"""
    return render_template("new_class.html", clss=Class.query.all())


@APP.route('/new_student', methods=['POST'])
def new_student():
    """To add new student"""
    if request.method == 'POST':
        print("Inside POST")
        try:
            student_id = request.form.get("student_id")
            name = request.form.get("name")
            class_id = request.form.get("class_id")
            time_stamp = time.time()
            timestamp = datetime.datetime.fromtimestamp(time_stamp)
            date_add = timestamp
            new_stud = Student(student_id, name, class_id, date_add, date_add)
            DB.session.add(new_stud)
            DB.session.commit()
            c_leader = request.form.get("c_leader")
            if c_leader == "yes":
                c_update = Class.query.filter_by(c_id=class_id).first()
                c_update.c_leader = student_id
                c_update.updated_on = date_add
                DB.session.add(c_update)
                DB.session.commit()
        except IOError:
            msg = "Error while adding new student"
            print(msg)
    return render_template('show_all.html', student=Student.query.all())


@APP.route("/add_new_student", methods=["GET", "POST"])
def add():
    """Add student function"""
    return render_template("new_student.html", clss=Class.query.all())


@APP.route('/update', methods=['POST'])
def update():
    """To perform update operation"""
    if request.method == 'POST':
        print("Inside Post")
        try:
            student_id = request.form.get("studentId")
            s_update = Student.query.filter_by(student_id=student_id).first()
            new_name = request.form.get("new_name")
            class_id = request.form.get("class_id")
            c_update = Class.query.filter_by(c_id=class_id).first()
            s_update.name = new_name
            s_update.class_id = class_id
            time_stamp = time.time()
            timestamp = datetime.datetime.fromtimestamp(time_stamp)
            s_update.updated_on = timestamp
            c_update.updated_on = timestamp
            DB.session.add(s_update)
            DB.session.add(c_update)
            DB.session.commit()
        except IOError:
            msg = "Error while updating"
            print(msg)
            return '<h1>Error while updating data</h1>'
    return redirect(url_for('show_all'))


@APP.route('/update_data', methods=["POST"])
def update_data():
    """Function to perfom update operation"""
    student_id = request.form.get("id")
    s_update = Student.query.filter_by(student_id=student_id).first()
    return render_template("update_data.html", student=s_update, cls=Class.query.all())


@APP.route("/delete", methods=["POST"])
def delete():
    """To perform delete operation"""
    student_id = request.form.get("id")
    student = Student.query.filter_by(student_id=student_id).first()
    try:
        DB.session.delete(student)
        DB.session.commit()
        return redirect(url_for('show_all'))
    except IOError:
        msg = "error during update operation"
        print(msg)


if __name__ == '__main__':
    DB.create_all()
    APP.run(debug=True)
