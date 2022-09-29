# todo list: make a function to ask user questions and able to store the answers for those questions
# show the user a list of locations (with picture and name), store their selection (for ex: user 1 - location2/ user 2 - location10/... in UserLocation table)

from audioop import reverse
from tkinter.tix import Select
from tokenize import String
from typing import final
from flask import Flask, redirect, url_for, render_template, request, session, flash, jsonify
from datetime import timedelta
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import func
from flask_login import UserMixin, login_user, LoginManager, login_required, logout_user, current_user
import argparse
import numpy as np

from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField, BooleanField, SelectField
from wtforms.validators import InputRequired, Length, ValidationError, EqualTo
from flask_bcrypt import Bcrypt
from collections import Counter

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
    boat_trips = db.Column(db.Integer, nullable=False)
    indigenous_tourism = db.Column(db.Integer, nullable=False)
    museums_and_culture_centres = db.Column(db.Integer, nullable=False)
    national_parks_and_protected_areas = db.Column(db.Integer, nullable=False)
    rural = db.Column(db.Integer, nullable=False)
    theme_parks = db.Column(db.Integer, nullable=False)
    urban_sightseeing = db.Column(db.Integer, nullable=False)
    water_activities = db.Column(db.Integer, nullable=False)
    winter_activities = db.Column(db.Integer, nullable=False)
    architecture_and_heritage = db.Column(db.Integer, nullable=False)
    arts = db.Column(db.Integer, nullable=False)
    culture = db.Column(db.Integer, nullable=False)
    excitement = db.Column(db.Integer, nullable=False)
    gastronomy = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.Integer, nullable=False)
    relaxation = db.Column(db.Integer, nullable=False)
    religious_tourism = db.Column(db.Integer, nullable=False)
    sports = db.Column(db.Integer, nullable=False)

class History(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    location = db.Column(db.String(100))

class Municipal(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    name = db.Column(db.String(100))

class Rating(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(100))
    location_id = db.Column(db.String(100))
    location_rating = db.Column(db.String(1))

    beach = db.Column(db.Integer, nullable=False)
    boat_trips = db.Column(db.Integer, nullable=False)
    indigenous_tourism = db.Column(db.Integer, nullable=False)
    museums_and_culture_centres = db.Column(db.Integer, nullable=False)
    national_parks_and_protected_areas = db.Column(db.Integer, nullable=False)
    rural = db.Column(db.Integer, nullable=False)
    theme_parks = db.Column(db.Integer, nullable=False)
    urban_sightseeing = db.Column(db.Integer, nullable=False)
    water_activities = db.Column(db.Integer, nullable=False)
    winter_activities = db.Column(db.Integer, nullable=False)
    architecture_and_heritage = db.Column(db.Integer, nullable=False)
    arts = db.Column(db.Integer, nullable=False)
    culture = db.Column(db.Integer, nullable=False)
    excitement = db.Column(db.Integer, nullable=False)
    gastronomy = db.Column(db.Integer, nullable=False)
    nature = db.Column(db.Integer, nullable=False)
    relaxation = db.Column(db.Integer, nullable=False)
    religious_tourism = db.Column(db.Integer, nullable=False)
    sports = db.Column(db.Integer, nullable=False)

class Image(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    location_name = db.Column(db.String(100), nullable=False)
    img_url = db.Column(db.String(100))

class Answer(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    user = db.Column(db.String(100))

    Q1 = db.Column(db.String(100), nullable=True)
    Q2 = db.Column(db.String(100), nullable=True)
    Q3 = db.Column(db.String(100), nullable=True)
    Q4 = db.Column(db.String(100), nullable=True)
    Q5 = db.Column(db.String(100), nullable=True)
    Q6 = db.Column(db.String(100), nullable=True)
    Q7 = db.Column(db.String(100), nullable=True)
    Q8 = db.Column(db.String(100), nullable=True)
    Q9 = db.Column(db.String(100), nullable=True)
    Q10 = db.Column(db.String(100), nullable=True)
    Q11 = db.Column(db.String(100), nullable=True)
    Q12 = db.Column(db.String(100), nullable=True)
    Q13 = db.Column(db.String(100), nullable=True)
    Q14 = db.Column(db.String(100), nullable=True)
    Q15 = db.Column(db.String(100), nullable=True)
    Q16 = db.Column(db.String(100), nullable=True)
    Q17 = db.Column(db.String(100), nullable=True)
    Q18 = db.Column(db.String(100), nullable=True)
    Q19 = db.Column(db.String(100), nullable=True)

class Form(FlaskForm):
    state = SelectField('state', choices=[
        ('AC', 'Acre'),
        ('AL', 'Alagoas'),
        ('AP', 'Amapá'),
        ('AM', 'Amazonas'),
        ('BA', 'Bahia'),
        ('CE', 'Ceará'),
        ('DF', 'Distrito Federal'),
        ('ES', 'Espírito Santo'),
        ('GO', 'Goiás'),
        ('MA', 'Maranhão'),
        ('MT', 'Mato Grosso'),
        ('MS', 'Mato Grosso do Sul'),
        ('MG', 'Minas Gerais'),
        ('PA', 'Pará'),
        ('PB', 'Paraíba'),
        ('PR', 'Paraná'),
        ('PE', 'Pernambuco'),
        ('PI', 'Piauí'),
        ('RJ', 'Rio de Janeiro'),
        ('RN', 'Rio Grande do Norte'),
        ('RS', 'Rio Grande do Sul'),
        ('RO', 'Rondônia'),
        ('RR', 'Roraima'),
        ('SC', 'Santa Catarina'),
        ('SP', 'São Paulo'),
        ('SE', 'Sergipe'),
        ('TO', 'Tocantins')])
    municipal = SelectField('municipal', choices=[])

@app.route('/municipal/<state>')
@login_required
def municipal(state):
    municipals = Municipal.query.filter_by(state=state).all()

    municipalArray = []

    for municipal in municipals:
        municipalObj = {}
        municipalObj['id'] = municipal.id
        municipalObj['name'] = municipal.name
        municipalArray.append(municipalObj)

    return jsonify({'municipals': municipalArray})


class RegisterForm(FlaskForm):
    username = StringField('username', validators=[
                           InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    confirm_password = PasswordField('confirm_password', validators=[
                                     InputRequired(), Length(min=8, max=80), EqualTo('password')])
    submit = SubmitField("Register")

    def validate_username(self, username):
        exsisting_user_username = User.query.filter_by(
            username=username.data).first()
        if exsisting_user_username:
            raise ValidationError(
                "That username already exist, please choose a different one.")


class LoginForm(FlaskForm):
    username = StringField(validators=[InputRequired(), Length(min=4, max=15)])
    password = PasswordField('password', validators=[
                             InputRequired(), Length(min=8, max=80)])
    remember = BooleanField('remember me')
    submit = SubmitField('Login')


@app.route("/")
def home():
    # remove Q1-19 from session before starting
    if 'recommended_id_list' in session: session.pop("recommended_id_list", None)
    if 'Q1' in session: session.pop("Q1", None)
    if 'Q2' in session: session.pop("Q2", None)
    if 'Q3' in session: session.pop("Q3", None)
    if 'Q4' in session: session.pop("Q4", None)
    if 'Q5' in session: session.pop("Q5", None)
    if 'Q6' in session: session.pop("Q6", None)
    if 'Q7' in session: session.pop("Q7", None)
    if 'Q8' in session: session.pop("Q8", None)
    if 'Q9' in session: session.pop("Q9", None)
    if 'Q10' in session: session.pop("Q10", None)
    if 'Q11' in session: session.pop("Q11", None)
    if 'Q12' in session: session.pop("Q12", None)
    if 'Q13' in session: session.pop("Q13", None)
    if 'Q14' in session: session.pop("Q14", None)
    if 'Q15' in session: session.pop("Q15", None)
    if 'Q16' in session: session.pop("Q16", None)
    if 'Q17' in session: session.pop("Q17", None)
    if 'Q18' in session: session.pop("Q18", None)

    if 'consent' in session: session.pop('consent', None)
    return render_template("welcome.html")


@app.route("/login", methods=["POST", "GET"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        user = User.query.filter_by(username=form.username.data).first()
        if user:  # if the username can be found in the database
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Login successful as {form.username.data}!', 'success')
                return redirect(url_for('Q0'))
            else:
                flash(
                    "Login unsuccessful, please check username and/or password", 'danger')
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
        return redirect(url_for('Q1'))

    if 'consent' in session:
        if session['consent'] == 'Accept':
            return render_template('register.html', form=form)
        if session['consent'] == 'Cancel':
            flash("You need to agree to our term in order to use this application", 'danger')
            return redirect(url_for('consent'))
    else:
        flash("You need to agree to our term in order to use this application", 'danger')
        return redirect(url_for('consent'))


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    session.clear()
    logout_user()
    return redirect(url_for("home"))


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template('welcome.html')


@app.route("/instruction", methods=["GET"])
def instruction():
    return render_template('instruction.html')

@app.route("/consent", methods=["POST", "GET"])
def consent():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')
        if len(answer) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('consent'))
        elif len(answer) == 2:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q0'))
        elif "Accept" in answer:
            session['consent'] = 'Accept'
            return redirect(url_for('register'))
        elif "Cancel" in answer:
            flash("You need to agree to our term in order to use this application", 'danger')
            session['consent'] = 'Cancel'
            return redirect(url_for('consent'))

    if current_user.is_authenticated:
        return redirect(url_for('Q0'))
    else:
        question = "By continuing, you agree to allow this app to use your data for scientific research purposes."
        answers = ['Accept', 'Cancel']
        return render_template('consent.html', question=question, answers=answers)


@app.route("/Q0", methods=["POST", "GET"])
@login_required
def Q0():
    # getting the time_looped for Q20
    session['times_looped'] = 0
    # remove Q1-19 from session before starting
    if 'recommended_id_list' in session: session.pop("recommended_id_list", None)
    if 'Q1' in session: session.pop("Q1", None)
    if 'Q2' in session: session.pop("Q2", None)
    if 'Q3' in session: session.pop("Q3", None)
    if 'Q4' in session: session.pop("Q4", None)
    if 'Q5' in session: session.pop("Q5", None)
    if 'Q6' in session: session.pop("Q6", None)
    if 'Q7' in session: session.pop("Q7", None)
    if 'Q8' in session: session.pop("Q8", None)
    if 'Q9' in session: session.pop("Q9", None)
    if 'Q10' in session: session.pop("Q10", None)
    if 'Q11' in session: session.pop("Q11", None)
    if 'Q12' in session: session.pop("Q12", None)
    if 'Q13' in session: session.pop("Q13", None)
    if 'Q14' in session: session.pop("Q14", None)
    if 'Q15' in session: session.pop("Q15", None)
    if 'Q16' in session: session.pop("Q16", None)
    if 'Q17' in session: session.pop("Q17", None)
    if 'Q18' in session: session.pop("Q18", None)

    print(session)

    if request.method == 'POST':
        answer = request.form.getlist('Q1')
        if len(answer) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('Q0'))
        elif len(answer) == 2:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q0'))
        elif "No - I am just curious to find out about destinations in general" in answer:
            return redirect(url_for('Q20'))
        elif "Yes - I want information for a specific trip" in answer:
            return redirect(url_for('Q1'))

    question = "Are you searching for a destination recommendation for a specific trip or just curious to find out about destinations in general?"
    answers = ['Yes - I want information for a specific trip', 'No - I am just curious to find out about destinations in general']
    return render_template('yesorno.html', question=question, answers=answers)


@app.route("/Q1", methods=["POST", "GET"])
@login_required
def Q1():
    if request.method == 'POST':
        categories = request.form.getlist('Q1')

        if len(categories) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('Q1'))
        else:
            # save the selected categories in session (associated key in session-dict: 'categories')
            session['categories'] = categories

            # store the answer into session to save later
            answer = ', '.join(categories)
            session['Q1'] = answer

            return redirect(url_for('Q2'))

    question = "What types of destinations are you interested to visit next?"
    answers = ['Cultural', 'Mountain', 'Nature', 'Rural', 'Beach', 'Urban']
    multiple_selection = True
    return render_template('Q1.html', question=question, answers=answers, multiple_selection=multiple_selection)


@app.route("/Q2", methods=["POST", "GET"])
@login_required
def Q2():
    Cultural = ['Arts', 'Urban sightseeing', 'Religious tourism', 'Architecture and heritage', 'Culture', 'Gastronomy', 'Indigenous tourism', 'Museums and cultural centres', 'Relaxation', 'Sports', 'Theme parks']
    Mountain = ['Beach', 'Sports', 'Relaxation', 'Water-based activities', 'Winter activities']
    Nature = ['Beach', 'Excitement', 'Sports', 'Water-based activities', 'Boat trips', 'Museums and cultural centres', 'Nature', 'Relaxation', 'National parks and protected areas']
    Rural = ['Beach', 'Sports', 'Relaxation', 'Rural', 'Water-based activities']
    Beach = ['Beach', 'Excitement', 'Sports', 'Water-based activities', 'Boat trips', 'Nature', 'Relaxation']
    Urban = ['Architecture and heritage', 'Urban sightseeing', 'Arts', 'Beach', 'Sports', 'Culture', 'Excitement', 'Nature', 'Relaxation', 'Museums and cultural centres', 'Theme parks']
    categories = []
    question = 'What activities are you searching for on your next trip?'
    answers = []

    final_dict = {
        'D_Cultural': 0,
        'D_Mountain': 0,
        'D_Nature': 0,
        'D_Rural': 0,
        'D_Beach': 0,
        'D_Urban': 0,
        'Beach': 0,
        'Boat trips': 0,
        'Indigenous tourism': 0,
        'Museums and cultural centres': 0,
        'National parks and protected areas': 0,
        'Rural': 0,
        'Theme parks': 0,
        'Urban sightseeing': 0,
        'Water-based activities': 0,
        'Winter activities': 0,
        'Architecture and heritage': 0,
        'Arts': 0,
        'Culture': 0,
        'Excitement': 0,
        'Gastronomy': 0,
        'Nature': 0,
        'Relaxation': 0,
        'Religious tourism': 0,
        'Sports': 0
    }

    if request.method == 'POST':
        # get all the selected tags from the form in Q2, then in final_dict change the value associated with the key "tag"
        list_of_tags = request.form.getlist('Q1')

        if len(list_of_tags) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('Q1'))
        else:
            # store the answer into session to save later
            answer = ', '.join(list_of_tags)
            session['Q2'] = answer

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

            # initiate the DRSModel
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
            session['recommended_id_list'] = recommended_id_list

            return redirect(url_for('Q3'))

    # if session['categories'] is not blank, which mean the user has chose some categories from Q1, then:
    if 'categories' in session:
        categories = session['categories']
        for category in categories:
            if category == 'Cultural':
                answers = answers + Cultural
                final_dict['D_Cultural'] = 1
            if category == 'Mountain':
                answers = answers + Mountain
                final_dict['D_Mountain'] = 1
            if category == 'Nature':
                answers = answers + Nature
                final_dict['D_Nature'] = 1
            if category == 'Rural':
                answers = answers + Rural
                final_dict['D_Rural'] = 1
            if category == 'Beach':
                answers = answers + Beach
                final_dict['D_Beach'] = 1
            if category == 'Urban':
                answers = answers + Urban
                final_dict['D_Urban'] = 1
        answers = set(answers)
        answers = sorted(answers)
        return render_template('Q1.html', question=question, answers=answers)
    else:
        flash("You have to answer this question before proceeding", 'danger')
        return redirect(url_for('Q1'))


@app.route('/Q3+4', methods=['GET', 'POST'])
@login_required
def Q3():
    form = Form()
    form.municipal.choices = [(municipal.id, municipal.name) for municipal in Municipal.query.filter_by(state='AC').all()]

    if request.method == "POST":
        municipal = Municipal.query.filter_by(id=form.municipal.data).first()

        # store the answer into session to save later
        session['Q3'] = form.state.data
        session['Q4'] = municipal.name

        return redirect(url_for('Q5'))
        # return 'State: {}, Municipal: {}'.format(form.state.data, municipal.name)

    question = "In which state do you live?"
    return render_template('QSelectField.html', form=form, question=question)


@app.route("/Q5", methods=["POST", "GET"])
@login_required
def Q5():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q5'))
        else:
            # store the answer into session to save later
            session['Q5'] = answer[0]

            return redirect(url_for('Q6'))

    question = "Which mode of transport are you planning to use on your next trip?"
    answers = ['Road [within a 500km radius]', 'Air [+500km radius]']
    return render_template('yesorno.html', question=question, answers=answers)


@app.route("/Q6", methods=["POST", "GET"])
@login_required
def Q6():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q6'))
        else:
            if 'kid' in answer:
                # store the answer into session to save later
                session['Q6'] = answer[0]

                return redirect(url_for('Q7'))
            # if there's no kid travelling, then skip Q7 and go straight to Q8
            else:
                # store the answer into session to save later
                session['Q6'] = answer[0]
                session['Q7'] = None

                return redirect(url_for('Q8'))

    question = "Who are you planning to travel with in your next trip?"
    answers = ['Couple', 'Couple with kids', 'Adult friends / Relatives', 'A larger group with kids', 'Alone']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q7", methods=["POST", "GET"])
@login_required
def Q7():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q7'))
        else:
            # immediately store the answer into session to save later
            session['Q7'] = answer[0]

            return redirect(url_for('Q8'))

    question = "How old are the youngest kids in the travel party?"
    answers = ['0-2 years', '3-5 years', '6-11 years', '12-17 years']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q8", methods=["POST", "GET"])
@login_required
def Q8():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q8'))
        else:
            # immediately store the answer into session to save later
            session['Q8'] = answer[0]

            return redirect(url_for('Q9'))

    question = "How many days do you plan to stay away on your next trip?"
    answers = ['1-4 days', '5-10 days', '11+ days']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q9", methods=["POST", "GET"])
@login_required
def Q9():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q9'))
        else:
            # immediately store the answer into session to save later
            session['Q9'] = answer[0]

            return redirect(url_for('Q10'))

    question = "How much is your budget for this trip?"
    answers = ['Less than R$ 1,000', 'R$ 1,000 to R$ 5,000', 'More than R$ 5,000']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q10", methods=["POST", "GET"])
@login_required
def Q10():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q10'))
        else:
            # immediately store the answer into session to save later
            session['Q10'] = answer[0]

            return redirect(url_for('Q11'))

    question = "What is your gender?"
    answers = ['Male', 'Female', 'Other / Prefer not to state']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q11", methods=["POST", "GET"])
@login_required
def Q11():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q11'))
        else:
            # immediately store the answer into session to save later
            session['Q11'] = answer[0]

            return redirect(url_for('Q12'))

    question = "What is your age?"
    answers = ['<10', '10-14', '15-20', '20-25', '25-30', '30-40', '40-50', '>50']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q12", methods=["POST", "GET"])
@login_required
def Q12():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q12'))
        else:
            # immediately store the answer into session to save later
            session['Q12'] = answer[0]

            return redirect(url_for('Q13'))

    question = "What is your highest level of education?"
    answers = ['No formal schooling', 'Elementary', 'High school', 'Graduate', 'Postgraduate', 'Prefer not to say']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q13", methods=["POST", "GET"])
@login_required
def Q13():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q13'))
        else:
            # immediately store the answer into session to save later
            session['Q13'] = answer[0]

            return redirect(url_for('Q14'))

    question = "What is your current relationship status?"
    answers = ['Single', 'De facto', 'Married', 'Divorced of Widowed', 'Prefer not to say']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q14", methods=["POST", "GET"])
@login_required
def Q14():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q14'))
        else:
            if 'Yes' in answer:
                # immediately store the answer into session to save later
                session['Q14'] = answer[0]

                return redirect(url_for('Q15'))
            # if there's no kid travelling, then skip Q15 and go straight to Q16
            else:
                # immediately store the answer into session to save later
                session['Q14'] = answer[0]
                session['Q15'] =  None

                return redirect(url_for('Q16'))

    question = "Do you have children?"
    answers = ['Yes', 'No']
    return render_template('yesorno.html', question=question, answers=answers)


@app.route("/Q15", methods=["POST", "GET"])
@login_required
def Q15():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q15'))
        else:
            # immediately store the answer into session to save later
            session['Q15'] = answer[0]

            return redirect(url_for('Q16'))

    question = "How old is your youngest kid?"
    answers = ['0-2 years', '3-5 years', '6-11 years', '12-17 years']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q16", methods=["POST", "GET"])
@login_required
def Q16():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q16'))
        else:
            # immediately store the answer into session to save later
            session['Q16'] = answer[0]

            return redirect(url_for('Q17'))

    question = "What is your household monthly income?"
    answers = ['R$ 0-500', 'R$ 500 - R$ 1000', 'R$ 1001 - R$ 2000', 'R$ 2001 - R$ 4000', 'R$ 4001 - R$ 8000', 'R$ 8001+']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q17", methods=["POST", "GET"])
@login_required
def Q17():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q17'))
        else:
            # immediately store the answer into session to save later
            session['Q17'] = answer[0]

            return redirect(url_for('Q18'))

    question = "How many states in Brazil have you visited?"
    answers = ['Only my own state', '2-4 states', '5-10 states', '10+ states']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q18", methods=["POST", "GET"])
@login_required
def Q18():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')

        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q18'))
        else:
            # immediately store the answer into session to save later
            session['Q18'] = answer[0]
            
            return redirect(url_for('Q19'))

    question = "How many countries have you been to?"
    answers = ['Only Brazil', '2-4 countries', '5-10 countries', '10+ countries']
    return render_template('Q1.html', question=question, answers=answers)

# func to check if a string has a number
def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)

@app.route("/Q19", methods=["POST", "GET"])
@login_required
def Q19():
    if request.method == 'POST':
        answer = request.form.getlist('QText')
        if len(answer[0]) == 0:
            flash("Destination name must not be blank", 'danger')
            return redirect(url_for('Q19'))
        elif has_numbers(answer[0]):
            flash("Destination name must not have numbers", 'danger')
            return redirect(url_for('Q19'))
        else:
            # get all answer from Q1 to Q19
            Q1 = session['Q1'] if 'Q1' in session else None
            Q2 = session['Q2'] if 'Q2' in session else None
            Q3 = session['Q3'] if 'Q3' in session else None
            Q4 = session['Q4'] if 'Q4' in session else None
            Q5 = session['Q5'] if 'Q5' in session else None
            Q6 = session['Q6'] if 'Q6' in session else None
            Q7 = session['Q7'] if 'Q7' in session else None
            Q8 = session['Q8'] if 'Q8' in session else None
            Q9 = session['Q8'] if 'Q9' in session else None
            Q10 = session['Q10'] if 'Q10' in session else None
            Q11 = session['Q11'] if 'Q11' in session else None
            Q12 = session['Q12'] if 'Q12' in session else None
            Q13 = session['Q13'] if 'Q13' in session else None
            Q14 = session['Q14'] if 'Q14' in session else None
            Q15 = session['Q15'] if 'Q15' in session else None
            Q16 = session['Q16'] if 'Q16' in session else None
            Q17 = session['Q17'] if 'Q17' in session else None
            Q18 = session['Q18'] if 'Q18' in session else None
            Q19 = answer[0]

            # store them in the database
            new_answer = Answer(user=current_user.id, 
                                Q1=Q1, 
                                Q2=Q2, 
                                Q3=Q3, 
                                Q4=Q4, 
                                Q5=Q5, 
                                Q6=Q6, 
                                Q7=Q7, 
                                Q8=Q8, 
                                Q9=Q9, 
                                Q10=Q10, 
                                Q11=Q11, 
                                Q12=Q12, 
                                Q13=Q13, 
                                Q14=Q14, 
                                Q15=Q15, 
                                Q16=Q16, 
                                Q17=Q17, 
                                Q18=Q18, 
                                Q19=Q19)
            db.session.add(new_answer)
            db.session.commit()

            return redirect(url_for('Q20'))

    question = "Which was the best destination you have been to?"
    return render_template('QText.html', question=question)

@app.route("/Q20", methods=["POST", "GET"])
@login_required
def Q20():
    # if we have recommended_id_list in session, which mean the user has answered Q1 and Q2:
    if 'recommended_id_list' in session:
        recommended_id_list = session['recommended_id_list']
    # if the user chose "random location recommendation func", then get random locations to recommend
    elif 'recommended_id_list' not in session:
        last_id = Location.query.count()
        random_id_list = random.sample(range(1, last_id), 10)
        random_location_list = []
        locations = Location.query.all()

        for location in locations:
            for i in random_id_list:
                if location.id == i:
                    random_location_list.append(location.id)
        recommended_id_list = random_location_list
    
    times_needed_to_loop = 3 # times_needed_to_loop = how many time do we need to loop Q20
    times_looped = session['times_looped']

    # loop through the recommended_id_list, if any locationId were found in the History table, remove that locationId from recommended_id_list
    for locationID in recommended_id_list:
        result = History.query.filter_by(user=current_user.id, location=locationID).first()
        if result is not None:
            # print(recommended_id_list)
            recommended_id_list.remove(int(result.location))
            # print(recommended_id_list)

    if request.method == 'POST':
        answer = request.form.getlist('Q20')

        # if the user choose both yes and no
        if "Yes" in answer and "No" in answer:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q20'))

        # if the user had been to this location before (yes)
        elif "Yes" in answer:
            # if the user press yes aka they had been to this location before, then create a new entry in the History table
            new_history = History(user=current_user.id, location=recommended_id_list[times_looped])
            db.session.add(new_history)
            db.session.commit()

            location = Location.query.filter_by(id=recommended_id_list[times_looped]).first()
            
            # get all the column names from the Location table
            activities = Location.__table__.columns.keys()
            # get all the activities from the column' names
            activities = activities[2:]
            temp_activities = []

            for activity in activities:
                count = getattr(location, activity)
                if count != 0:
                    temp_activities.append(activity)

            # determine if count of temp_activities > 8 or not, if not then pass all 8, descending count
            if len(temp_activities) <= 8:
                final_activities = temp_activities # do nothing
            elif len(temp_activities) > 8:
                final_activities = []
                # find top 3 labels, call top_3
                top_3 = []
                # creating a list of count of all activities
                count_list = []
                for activity in temp_activities:
                    count = getattr(location, activity)
                    count_list.append(count)
                # create a list of tuples, sort that tuple (sort always sort by 1st element of a tuple), get top 3 tuples
                top_3_tuples = sorted(zip(count_list, temp_activities), reverse=True)[:3]
                # loop through the tuples, append the top 3 activities
                for i in top_3_tuples:
                    top_3.append(i[1])
                # pick random 1 of the 3
                final_activities.append(random.choice(top_3))
                top_3.remove(final_activities[0])
                temp_activities.remove(final_activities[0])
                # pick random 1 of the remaining 2 in top_3
                final_activities.append(random.choice(top_3))
                temp_activities.remove(final_activities[1])

                # find all labels with freq > 2 (not including the 2 chosen one above), called freq_more_than_2
                freq_more_than_2 = []
                for activity in temp_activities:
                    count = getattr(location, activity)
                    if count >=2:
                        freq_more_than_2.append(activity)
                # continue to pick from freq_more_than_2 until got 6 labels (activities) in total or there's no more activities in freq_more_than_2
                while len(freq_more_than_2) > 0 and len(final_activities) < 6:
                    # pick 1 random from freq_more_than_2
                    random_activity = random.choice(freq_more_than_2)
                    final_activities.append(random_activity)
                    freq_more_than_2.remove(random_activity)
                    temp_activities.remove(random_activity)

                # pick 1 random from the remaining labels (not including the chosen 6), keep picking until got 8 labels
                while len(final_activities) != 8:
                    random_activity = random.choice(temp_activities)
                    final_activities.append(random_activity)
                    temp_activities.remove(random_activity)


            # getting the images of the current location
            img_data = Image.query.filter_by(location_name=location.name).all()
            images = []
            for i in img_data:
                images.append(i.img_url)

            # converting the final_activities so that it's more human-readable
            count = 0
            for activity in final_activities:
                activity = activity.replace('_', ' ')
                final_activities[count] = activity
                count += 1
            session['final_activities'] = final_activities
            session['current_location_name'] = location.name
            session['current_location_id'] = location.id
            session['images'] = images
            return redirect(url_for('DestinationEvaluation'))

        # if the user has not been to this location before (no)
        elif "No" in answer and times_looped != times_needed_to_loop:
            location = Location.query.filter_by(id=recommended_id_list[times_looped]).first()
            location_name = location.name     

            avg = {}
            # query all average ratings of all activities belong to that location
            ratings = Rating.__table__.columns.keys()
            ratings = ratings[4:]

            # get all rating belongs to the current location
            all_rating_of_current_location = Rating.query.filter_by(location_id=location.id).all()

            # get the average rating of a location:
            sum = 0
            count = 0
            for i in all_rating_of_current_location:
                score = i.location_rating
                if score != 0:
                    sum = sum + score
                    count += 1
            if count != 0:
                location_average_rating = sum / count
            elif count == 0:
                location_average_rating = 0

            # loop through all rating, we'll add key-value pair (rating-avg_rating) to the avg dict with each loop
            for rating in ratings:
                sum = 0
                count = 0
                for i in all_rating_of_current_location:
                    score = getattr(i, rating)
                    # we only count if the rating is not 0, 0 means that no one has rated that location, or any location related activities yet
                    if score != 0:
                        sum = sum + score
                        count += 1
                # if we found out that indeed there had been rating for this location, then add the activity-avg_rating to the avg dict
                if count != 0:
                    avg[f'{rating}'] = sum / count
                # if we can't find any rating for that location, then just give the default value of 0
                elif count == 0:
                    avg[f'{rating}'] = 0

            # getting the top 3 pairs (highest value aka average rating) in avg dict
            c = Counter(avg)
            top_three_activities = c.most_common(3)  # returns top 3 pairs
            formatted_top_3_activities = {}
            for activity in top_three_activities:
                new_key = activity[0].replace('_', ' ')
                formatted_top_3_activities[f'{new_key}'] = activity[1]

            # getting the images of the current location
            img_data = Image.query.filter_by(location_name=location.name).all()
            images = []
            for i in img_data:
                images.append(i.img_url)

            # create a dict for those 3 activities
            session['times_looped'] += 1
            return render_template('DestinationDetail.html', location=location_name, top_three_activities=formatted_top_3_activities, images=images)

    question = "Have you been to this destination?"
    answers = ['Yes', 'No']
    location = Location.query.filter_by(id=recommended_id_list[times_looped]).first()
    location = location.name
    if times_looped != times_needed_to_loop:
        return render_template('Q20.html', question = question, location = location, answers = answers)
    elif times_looped == times_needed_to_loop:
        return redirect(url_for('Q21'))

@app.route("/DestinationEvaluation", methods=["POST", "GET"])
@login_required
def DestinationEvaluation():
    if request.method == 'POST':
        # data is where we will store all rating scores
        data = {}

        # getting the list of rating for the "location rating" part
        location_rate = request.form.getlist('location-rate')
        # if the user rated the location (1-7 star(s)), then add that key-value pair to the dict
        if len(location_rate) != 0:
            data['location_rating'] = location_rate[0]
        # if the user didn't rate (0 star), then add the key-value (value = 0) to the dict
        elif len(activity_rate) == 0:
            data['location_rating'] = '0'

        final_activities = session['final_activities']
        # loop through the list of 8 (ideally) activities being rated in the DestinationEvaluation route, get the corresponding rating from the form, then create new key-value pairs in data dict accordingly
        for activity in final_activities:
            activity_rate = request.form.getlist(f'{activity}')
            # print(activity_rate)
            if len(activity_rate) != 0:
                data[f'{activity}'] = activity_rate[0]
            elif len(activity_rate) == 0:
                data[f'{activity}'] = '0'

        # create a new Rating row (record), if we can find the key (activity), then use the associated value, if not we assume the user rated 0 for that activity 
        # 0 in Rating table means that there's no rating for that activity yet, not rating of 0 (worst)
        new_rating = Rating(user=current_user.id, 
                            location_id=session['current_location_id'],
                            location_rating = data.get('location_rating', '0'),

                            beach = data.get('beach', '0'),
                            boat_trips = data.get('boat trips', '0'),
                            indigenous_tourism = data.get('indigenous tourism', '0'),
                            museums_and_culture_centres = data.get('museums and culture_centres', '0'),
                            national_parks_and_protected_areas = data.get('national parks and protected_areas', '0'),
                            rural = data.get('rural', '0'),
                            theme_parks = data.get('theme parks', '0'),
                            urban_sightseeing = data.get('urban sightseeing', '0'),
                            water_activities = data.get('water activities', '0'),
                            winter_activities = data.get('winter activities', '0'),
                            architecture_and_heritage = data.get('architecture and_heritage', '0'),
                            arts = data.get('arts', '0'),
                            culture = data.get('culture', '0'),
                            excitement = data.get('excitement', '0'),
                            gastronomy = data.get('gastronomy', '0'),
                            nature = data.get('nature', '0'),
                            relaxation = data.get('relaxation', '0'),
                            religious_tourism = data.get('religious tourism', '0'),
                            sports = data.get('sports', '0')
                            )
        db.session.add(new_rating)
        db.session.commit()

        return redirect(url_for('Q20'))

    question='Rate this destination'
    location_name = session['current_location_name']
    final_activities = session['final_activities']
    images= session['images']
    
    return render_template('DestinationEvaluation.html', location_name=location_name, question=question, final_activities=final_activities, images=images)

@app.route("/Q21", methods=["POST", "GET"])
@login_required
def Q21():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')
        if len(answer) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q21'))
        elif "Yes" in answer:
            return redirect(url_for('Q0'))
        elif "No" in answer:
            return redirect(url_for('welcome'))

    question = "Would you like to be recommended more destinations?"
    answers = ['Yes', 'No']
    return render_template('yesorno.html', question=question, answers=answers)

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