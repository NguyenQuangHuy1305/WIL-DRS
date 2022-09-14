# todo list: make a function to ask user questions and able to store the answers for those questions
# show the user a list of locations (with picture and name), store their selection (for ex: user 1 - location2/ user 2 - location10/... in UserLocation table)

from audioop import reverse
from tokenize import String
from flask import Flask, redirect, url_for, render_template, request, session, flash
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import argparse
import numpy as np

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt

import random
from model import DRSModel

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

class User(db.Model, UserMixin):
    id = db.Column("id", db.Integer, primary_key=True)
    username = db.Column(db.String(100), nullable=False, unique=True)
    password = db.Column(db.String(100), nullable=False)

class Location(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
    beach = db.Column(db.Integer, nullable=False)
    boatTrips = db.Column(db.Integer, nullable=False)
    indigenousTourism = db.Column(db.Integer, nullable=False)
    museumsAndCultureCentres = db.Column(db.Integer, nullable=False)
    nationalParksAndProtectedAreas = db.Column(db.Integer, nullable=False)
    rural = db.Column(db.Integer, nullable=False)
    themeParks = db.Column(db.Integer, nullable=False)
    urbanSightseeing = db.Column(db.Integer, nullable=False)
    waterActivities = db.Column(db.Integer, nullable=False)
    winterActivities = db.Column(db.Integer, nullable=False)
    architectureAndHeritage = db.Column(db.Integer, nullable=False)
    arts = db.Column(db.Integer, nullable=False)
    culture = db.Column(db.Integer, nullable=False)
    excitement = db.Column(db.Integer, nullable=False)
    gastronomy = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.Integer, nullable=False)
    relaxation = db.Column(db.Integer, nullable=False)
    religiousTourism = db.Column(db.Integer, nullable=False)
    sports = db.Column(db.Integer, nullable=False)

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
        if user: # if the username can be found in the database
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Login successful as {form.username.data}!', 'success')
                return redirect(url_for('home'))
            else:
                flash("Login unsuccessful, please check username and/or password", 'danger')
        else:
            flash("Login unsuccessful, please check username and/or password", 'danger')
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
    session.pop("categories", None)
    logout_user()
    flash(f'Log out successful!', 'success')
    return redirect(url_for("home"))

@app.route("/surpriseme")
@login_required
def surpriseme():
    last_id = Location.query.count()
    random_id_list = random.sample(range(1, last_id), 10)
    random_location_list = []
    locations = Location.query.all()

    for location in locations:
        for i in random_id_list:
            if location.id == i:
                random_location_list.append(location.name)

    return render_template("supriseme.html", locations=random_location_list)

@app.route("/Q1", methods=["POST", "GET"])
@login_required
def Q1():
    if request.method == 'POST':
        categories = request.form.getlist('Q1')
        print(categories)
        # save the selected categories in session (associated key in session-dict: 'categories')
        session['categories'] = categories
        return redirect(url_for('Q2'))
    return render_template('Q1.html')

@app.route("/Q2", methods=["POST", "GET"])
@login_required
def Q2():
    cultural = ['Arts', 'Urban sightseeing', 'Religious tourism', 'Architecture and heritage', 'Culture', 'Gastronomy', 'Indigenous tourism', 'Museums and cultural centres', 'Relaxation', 'Sports', 'Theme parks']
    mountain = ['Beach', 'Sports', 'Relaxation', 'Water-based activities', 'Winter activities']
    nature = ['Beach', 'Excitement', 'Sports', 'Water-based activities', 'Boat trips', 'Museums and cultural centres', 'Nature', 'Relaxation', 'National parks and protected areas']
    rural = ['Beach', 'Sports', 'Relaxation', 'Rural', 'Water-based activities']
    beach = ['Beach', 'Excitement', 'Sports', 'Water-based activities', 'Boat trips', 'Nature', 'Relaxation']
    urban = ['Architecture and heritage', 'Urban sightseeing', 'Arts', 'Beach', 'Sports', 'Culture', 'Excitement', 'Nature', 'Relaxation', 'Museums and cultural centres', 'Theme parks']
    categories = []
    tags = []

    final_dict = {
        'D_Cultural' : 0,
        'D_Mountain' : 0,
        'D_Nature' : 0,
        'D_Rural' : 0,
        'D_Beach' : 0,
        'D_Urban' : 0,
        'Beach' : 0,
        'Boat trips' : 0,
        'Indigenous tourism' : 0,
        'Museums and cultural centres' : 0,
        'National parks and protected areas' : 0,
        'Rural' : 0,
        'Theme parks' : 0,
        'Urban sightseeing' : 0,
        'Water-based activities' : 0,
        'Winter activities' : 0,
        'Architecture and heritage' : 0,
        'Arts' : 0,
        'Culture' : 0,
        'Excitement' : 0,
        'Gastronomy' : 0,
        'Nature' : 0,
        'Relaxation' : 0,
        'Religious tourism' : 0,
        'Sports' : 0
    }

    if request.method == 'POST':
        # get all the selected tags from the form in Q2, then in final_dict change the value associated with the key "tag"
        list_of_tags = request.form.getlist('Q2')
        for tag in list_of_tags:            
            final_dict[tag] = 1

        # get the categories from session (created in Q1), loop through the list categories, change final_dict's value from 0 to 1 for each category (key)
        categories = session['categories']
        for category in categories:
            if category == 'cultural':
                final_dict['D_Cultural'] = 1
            if category == 'mountain':
                final_dict['D_Mountain'] = 1
            if category == 'nature':
                final_dict['D_Nature'] = 1
            if category == 'rural':
                final_dict['D_Rural'] = 1
            if category == 'beach':
                final_dict['D_Beach'] = 1
            if category == 'urban':
                final_dict['D_Urban'] = 1

        # convert the final_dict's value to a list
        final_list = list(final_dict.values())
        final_list = np.array(final_list)

        parser = argparse.ArgumentParser()
        parser.add_argument('--filepath', default='./Destination_tags_sum.csv')
        parser.add_argument('--model', default='./drs_model')
        config = parser.parse_args()
        model = DRSModel(config)

        # use predict function from model.py to get recommendation, but the return is a tuple, 2nd element in that tuple is the np.array we need
        result = model.predict(final_list)
        print(result)
        # that np.array will be converted to python list for easier access
        result = np.ndarray.tolist(result[1][0])
        # since the returned list is in reverse order (lowest to highest probability) --> we need to reverse the list
        result.reverse()

        recommended_id_list = result
        recommended_location_list = []

        for i in recommended_id_list:
            location = Location.query.filter_by(id=i).first()
            recommended_location_list.append(location.name)

        return render_template("recommendation.html", locations=recommended_location_list)

    if 'categories' in session:
        categories = session['categories']
        for category in categories:
            if category == 'cultural':
                tags = tags + cultural
                final_dict['D_Cultural'] = 1
            if category == 'mountain':
                tags = tags + mountain
                final_dict['D_Mountain'] = 1
            if category == 'nature':
                tags = tags + nature
                final_dict['D_Nature'] = 1
            if category == 'rural':
                tags = tags + rural
                final_dict['D_Rural'] = 1
            if category == 'beach':
                tags = tags + beach
                final_dict['D_Beach'] = 1
            if category == 'urban':
                tags = tags + urban
                final_dict['D_Urban'] = 1
        tags = set(tags)
        tags = sorted(tags)
        return render_template('Q2.html', tags=tags)
    else:
        return f"you haven't answer 1st question"


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