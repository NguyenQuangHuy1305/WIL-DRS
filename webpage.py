from tokenize import String
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt

import random

app = Flask(__name__)
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)

# config for the table users
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
# do not track modifications to the db (maybe to get rid of notifications)
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# secret key
app.config['SECRET_KEY'] = 'test_secret_key'

# app.permanent_session_lifetime = timedelta(days=5)

login_manager = LoginManager()
login_manager.init_app(app)
login_manager.login_view = "login"

@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))

# class LoginForm(FlaskForm):
#     username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
#     password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
#     remember = BooleanField('remember me')

class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

    # def __init__(self, name, email):
    #     self.username = username
    #     self.password = password

class Location(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    urban = db.Column(db.Integer, nullable=False)
    rural = db.Column(db.Integer, nullable=False)
    canyonvalleys = db.Column(db.Integer, nullable=False)
    mountain = db.Column(db.Integer, nullable=False)
    water = db.Column(db.Integer, nullable=False)
    summer = db.Column(db.Integer, nullable=False)
    winter = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.Integer, nullable=False)
    park = db.Column(db.Integer, nullable=False)
    wildlife = db.Column(db.Integer, nullable=False)
    relax = db.Column(db.Integer, nullable=False)
    entertainment = db.Column(db.Integer, nullable=False)
    nightlife = db.Column(db.Integer, nullable=False)
    ethnic = db.Column(db.Integer, nullable=False)
    culture = db.Column(db.Integer, nullable=False)
    festival = db.Column(db.Integer, nullable=False)
    gastronomy = db.Column(db.Integer, nullable=False)
    religion = db.Column(db.Integer, nullable=False)
    sports = db.Column(db.Integer, nullable=False)
    adventure = db.Column(db.Integer, nullable=False)
    fishing = db.Column(db.Integer, nullable=False)

class RegisterForm(FlaskForm):
    username = StringField('username', validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('confirm_password', validators=[InputRequired(), Length(min=8, max=80), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        exsisting_user_username = User.query.filter_by(
            username=username.data).first()
        if exsisting_user_username:
            raise ValidationError("That username already exist, please choose a different one.")

class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')


@app.route("/")
def home():
    return render_template("index.html")

# @app.route("/<name>")
# def user(name):
#     return f"Hello {name}!"

@app.route("/view")
def view():
    return render_template("view.html", values=User.query.all())

@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Login successful as {form.username.data}!', 'success')
                return redirect(url_for('home'))
            else:
                flash("login unsuccessful, please check username and/or password", 'danger')
    return render_template('login.html', form=form)

@app.route('/register', methods=["POST", "GET"])
def register():
    form = RegisterForm()

    if form.validate_on_submit():
        hashed_password = bcrypt.generate_password_hash(form.password.data)
        new_user = User(username=form.username.data, password=hashed_password)
        db.session.add(new_user)
        db.session.commit()
        flash(f'Account created for {form.username.data}!', 'success')
        return redirect(url_for('home'))

    return render_template('register.html', form=form)

@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    logout_user()
    flash(f'Log out successful!', 'success')
    return redirect(url_for("home"))

@app.route("/surpriseme")
def surpriseme():
    last_id = Location.query.count()
    random_id_list = random.sample(range(1, last_id), 9)
    random_location_list = []
    locations = Location.query.all()

    for location in locations:
        for i in random_id_list:
            if location.id == i:
                random_location_list.append(location.name)
    
    return render_template("supriseme.html", locations=random_location_list)



# @app.route("/login", methods=["POST", "GET"])
# def login():
#     if request.method == "POST":
#         session.permanent = True
#         user = request.form["nm"]
#         session["user"] = user

#         found_user = users.query.filter_by(name=user).first()
#         if found_user:
#             session["email"] = found_user.email
#         else:
#             usr = users(user, "")
#             db.session.add(usr)
#             db.session.commit()

#         # flash("Login successful!")
#         return redirect(url_for("home"))
#     else:
#         if "user" in session:
#             # flash("Already logged in!")
#             return redirect(url_for("user"))
#         return render_template("login.html")

# @app.route("/signup", methods=["POST", "GET"])
# def signup(): 

# @app.route("/user", methods=["POST", "GET"])
# def user():
#     email = None
#     if "user" in session:
#         user = session["user"]

#         if request.method == "POST":
#             email = request.form["email"]
#             session["email"] = email
#             found_user = users.query.filter_by(name=user).first()
#             found_user.email = email
#             db.session.commit()
#             # flash("Email was saved!")
#         else:
#             if "email" in session:
#                 email = session["email"]

#         return render_template("user.html", email=email, user=user)
#     else:
#         flash("You are not logged in!")
#         return redirect(url_for("login"))

# @app.route("/admin")
# def admin():
#     return redirect(url_for("user", name="you're not admin!"))

if __name__ == "__main__":
    db.create_all()
    app.run(debug=True)