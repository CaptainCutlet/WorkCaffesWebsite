from flask import Flask, url_for, redirect, request, render_template, flash
from flask_sqlalchemy import SQLAlchemy
from flask_login import UserMixin, login_user, LoginManager, login_required, current_user, logout_user
import os
from flask_bootstrap import Bootstrap
from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField, TimeField
from wtforms.validators import DataRequired, URL
from forms import CafeForm, LoginForm, RegisterForm
from werkzeug.security import generate_password_hash, check_password_hash

# Flaks config
app = Flask(__name__)

# Add Bootstrap to this app
Bootstrap(app)

# Database config
app.config['SECRET_KEY'] = os.environ['db_secret_key']
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///data.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

# Authentication
login_manager = LoginManager()
login_manager.init_app(app)


# Class for User
class User(UserMixin, db.Model):
    __tablename__ = 'user'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(25), unique=False)
    surname = db.Column(db.String(25), unique=False)
    username = db.Column(db.String(25), unique=True)
    email = db.Column(db.String(200), unique=True)
    password_hash = db.Column(db.String(250), unique=False)

    def check_hash(self, password):
        return check_password_hash(self.password_hash, password)


# Main caffe class for DB
class Caffe(UserMixin, db.Model):
    __tablename__ = 'caffe'
    id = db.Column(db.Integer, primary_key=True)
    caffe = db.Column(db.String(100), unique=True)
    wifi = db.Column(db.String(15), unique=False)
    chargers = db.Column(db.String(15), unique=False)
    env = db.Column(db.String(15), unique=False)
    serv_food = db.Column(db.String(15), unique=False)
    price = db.Column(db.String(15), unique=False)
    # Connection to parent (Caffe) database
    parent_id = db.Column(db.Integer, db.ForeignKey('user.id'))
    parent = db.relationship('User', backref=db.backref('caffes', lazy=True))


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


@app.route("/")
def home():
    if current_user.is_authenticated:
        caffe_list = db.session.query(Caffe).all()
        return render_template("index.html", cafes=caffe_list)
    else:
        form = LoginForm()
        return render_template('login.html', form=form)


@app.route("/login", methods=['POST', 'GET'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        matching_user = db.session.query(User).filter_by(email=form.email.data).first()
        if matching_user and matching_user.check_hash(form.password.data):
            login_user(matching_user)
            return redirect(url_for("home"))
        else:
            flash('Invalid email or password')
            return redirect('login')
    return render_template('login.html', form=form)


@app.route("/register", methods=['POST', 'GET'])
def register():
    form = RegisterForm()
    if form.validate_on_submit():
        new_user = User(
            name=form.name.data,
            surname=form.surname.data,
            email=form.email.data,
            username=form.username.data,
            password_hash=generate_password_hash(password=form.password.data, salt_length=8)
        )
        db.session.add(new_user)
        db.session.commit()
        login_user(new_user)
        return redirect(url_for("home"))
    return render_template('register.html', form=form)


@app.route("/logout", methods=['POST', 'GET'])
def logout():
    login_user(current_user)
    return redirect(url_for("login"))


@app.route("/add_cafe", methods=['GET', 'POST'])
def add_cafe():
    form = CafeForm()
    error = None
    caffes_list = db.session.query(Caffe).all()
    if form.validate_on_submit() and request.method == 'POST':
        name = form.name.data
        chargers = form.chargers.data
        price = form.price.data
        env = form.env.data
        serv_food = form.serv_food.data
        wifi = form.wifi.data

        # Checking whether caffe already exists in the database
        for caffe in caffes_list:
            if name == caffe.caffe:
                error = 'This caffe already exists!'
                flash(error)
                return redirect(url_for("add_cafe", cafe_form=form))

        # Adding caffe if one doesn't exist
        if error is None:
            new_caffe = Caffe(
                caffe=name,
                wifi=wifi,
                chargers=chargers,
                env=env,
                serv_food=serv_food,
                price=price,
                parent=current_user)
            db.session.add(new_caffe)
            db.session.commit()
            return redirect(url_for("home"))

    return render_template("add_cafe.html", cafe_form=form)


if __name__ == "__main__":
    app.run(debug=True)