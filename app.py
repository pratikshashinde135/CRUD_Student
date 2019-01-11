from flask import Flask, render_template, redirect, url_for, request
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InputRequired, Email, Length
from flask_sqlalchemy import SQLAlchemy
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import LoginManager, UserMixin, login_user, login_required, logout_user
import time
import datetime
import pymysql

pymysql.install_as_MySQLdb()

app = Flask(__name__)
app.config['SECRET_KEY'] = 'Thisissupposedtobesecret!'
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql://root:pratiksha@localhost/mydb'
bootstrap = Bootstrap(app)
db = SQLAlchemy(app)
login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = 'login'


# creating user table
class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(15), unique=True)
    email = db.Column(db.String(50), unique=True)
    password = db.Column(db.String(80))

    def __init__(self, username, email, password):
        self.username = username
        self.email = email
        self.password = password



@login_manager.user_loader
def load_user(id):
    return User.query.get(int(id))


# get data from login page
class LoginForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')


# get data from login page
class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    email = StringField('email', validators=[InputRequired(), Email(message='Invalid email'), Length(max=50)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    db.create_all()


@app.route('/')
def index():
    return render_template('index.html')

# login
@app.route('/login', methods=['GET', 'POST'])
def login():
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


# signup
@app.route('/signup', methods=['GET', 'POST'])
def signup():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = generate_password_hash(form.password.data, method='sha256')
        new_user = User(username=form.username.data, email=form.email.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()

        return '<h1>New user has been created!</h1>'
        # return '<h1>' + form.username.data + ' ' + form.email.data + ' ' + form.password.data + '</h1>'
    return render_template('signup.html', form=form)


class Student(db.Model):
    student_id = db.Column('id', db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    class_id = db.Column(db.Integer, db.ForeignKey('class.c_id'))
    created_on = db.Column(db.String(50))
    updated_on = db.Column(db.String(50))

    # clas = db.relationship('Class', backref='student', lazy=True)

    def __init__(self, student_id, name, class_id, created_on, updated_on):
        self.student_id = student_id
        self.name = name
        self.class_id = class_id
        self.created_on = created_on
        self.updated_on = updated_on


class Class(db.Model):
    c_id = db.Column(db.Integer, primary_key=True)
    c_name = db.Column(db.String(100))
    c_leader = db.Column(db.Integer, db.ForeignKey('student.id'))
    created_on = db.Column(db.String(50))
    updated_on = db.Column(db.String(50))

    # students = db.relationship('Student', backref='class', lazy=True)

    def __init__(self, c_id, c_name, c_leader, created_on, updated_on):
        self.c_id = c_id
        self.c_name = c_name
        self.c_leader = c_leader
        self.created_on = created_on
        self.updated_on = updated_on
        db.create_all()


@app.route('/show_all')
@login_required
def show_all():
    return render_template('show_all.html', student=Student.query.all())


# creating new student data
@app.route('/new_student', methods=['POST'])
def new_student():
    if request.method == 'POST':
        print("Inside POST")
        try:
            studentId = request.form.get("studentId")
            name = request.form.get("name")
            classId = request.form.get("classId")
            cName = request.form.get("cName")
            ts = time.time()
            timestamp = datetime.datetime.fromtimestamp(ts)
            dateadd = timestamp
            new_stud = Student(studentId, name, classId, dateadd, dateadd)
            db.session.add(new_stud)
            db.session.commit()
            c_leader = request.form.get("c_leader")
            if c_leader == "yes":
                c_leader = studentId
                new_class = Class(classId, cName, c_leader, dateadd, dateadd)
                db.session.add(new_class)
                db.session.commit()
            else:
                new_class = Class(c_id=classId,c_name=cName, created_on=dateadd, updated_on=dateadd)
                db.session.add(new_class)
                db.session.commit()


        except:
            msg = "Error while adding new student"
            print(msg)
    return render_template('show_all.html', student=Student.query.all())


# Add a new student record
@app.route("/add_new_student", methods=["GET", "POST"])
def add():
    return render_template("new_student.html", clss=Class.query.all())


# update student data
@app.route('/update', methods=['POST'])
def update():
    if request.method == 'POST':
        student_id = request.form.get("studentId")
        sUpdate = Student.query.filter_by(student_id=student_id).first()
        newName = request.form.get("newName")
        classId = request.form.get("classId")
        cUpdate = Class.query.filter_by(c_id=classId).first()
        sUpdate.name = newName
        sUpdate.class_id = classId
        ts = time.time()
        timestamp = datetime.datetime.fromtimestamp(ts)
        sUpdate.updated_on = timestamp
        cUpdate.updated_on = timestamp
        db.session.add(sUpdate)
        db.session.add(cUpdate)
        db.session.commit()
    return redirect(url_for('show_all'))


# Perform Update Operation
@app.route('/updatedata', methods=["POST"])
def updatedata():
    student_id = request.form.get("id")
    sUpdate = Student.query.filter_by(student_id=student_id).first()
    return render_template("updatedata.html", student=sUpdate, cls=Class.query.all())


# Perform Delete Operation
@app.route("/delete", methods=["POST"])
def delete():
    student_id = request.form.get("id")
    student = Student.query.filter_by(student_id=student_id).first()
    try:
        db.session.delete(student)
        db.session.commit()
        return redirect(url_for('show_all'))
    except:
        msg = "error during update operation"
        print(msg)
        return redirect(url_for('show_all'))


@app.route('/logout')
@login_required
def logout():
    logout_user()
    return redirect(url_for('index'))


if __name__ == '__main__':
    db.create_all()
    app.run(debug=True)

