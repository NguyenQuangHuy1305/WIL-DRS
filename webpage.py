# todo list: make a function to ask user questions and able to store the answers for those questions
# show the user a list of locations (with picture and name), store their selection (for ex: user 1 - location2/ user 2 - location10/... in UserLocation table)

from audioop import reverse
from tkinter.tix import Select
from tokenize import String
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


class Municipal(db.Model):
    id = db.Column("id", db.Integer, primary_key=True)
    state = db.Column(db.String(2))
    name = db.Column(db.String(100))


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


@app.route('/Q4', methods=['GET', 'POST'])
def Q4():
    form = Form()
    form.municipal.choices = [(municipal.id, municipal.name)
                              for municipal in Municipal.query.filter_by(state='AC').all()]

    if request.method == "POST":
        municipal = Municipal.query.filter_by(id=form.municipal.data).first()
        return 'State: {}, Municipal: {}'.format(form.state.data, municipal.name)

    question = "In which state do you live?"
    return render_template('QSelectField.html', form=form, question=question)


@app.route('/municipal/<state>')
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
    return render_template("welcome.html")

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
        if user:  # if the username can be found in the database
            if bcrypt.check_password_hash(user.password, form.password.data):
                login_user(user)
                flash(f'Login successful as {form.username.data}!', 'success')
                return redirect(url_for('Q1'))
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

    return render_template('register.html', form=form)


@app.route("/logout", methods=["POST", "GET"])
@login_required
def logout():
    session.pop("categories", None)
    logout_user()
    flash(f'Log out successful!', 'success')
    return redirect(url_for("home"))


@app.route("/welcome", methods=["GET"])
def welcome():
    return render_template('welcome.html')


@app.route("/instruction", methods=["GET"])
def instruction():
    return render_template('instruction.html')

@app.route("/consent", methods=["GET"])
def consent():
    return render_template('consent.html')

@app.route("/Q20", methods=["GET"])
@login_required
def Q20():
    # Please retrieve a location image here and pass to the frontend page.
    question = "Have you been to this destination?"
    answers = ['Yes', 'No']
    return render_template('Q20.html', question=question, answers=answers)

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


@app.route("/Q0", methods=["POST", "GET"])
@login_required
def Q0():
    if request.method == 'POST':
        answer = request.form.getlist('Q1')
        if len(answer) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('Q0'))
        elif "Yes - I want information for a specific trip" in answer and "No - I am just curious to find out about destinations in general" in answer:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q0'))
        elif "No - I am just curious to find out about destinations in general" in answer:
            return redirect(url_for('surpriseme'))
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
        print(categories)
        if len(categories) == 0:
            flash("Please choose 1 option", 'danger')
            return redirect(url_for('Q1'))
        else:
            # save the selected categories in session (associated key in session-dict: 'categories')
            session['categories'] = categories
            return redirect(url_for('Q2'))

    question = "What types of destinations are you interested to visit next?"
    answers = ['Cultural', 'Mountain', 'Nature', 'Rural', 'Beach', 'Urban']
    multiple_selection = True
    return render_template('Q1.html', question=question, answers=answers, multiple_selection=multiple_selection)

@app.route("/Q2", methods=["POST", "GET"])
@login_required
def Q2():
    Cultural = ['Arts', 'Urban sightseeing', 'Religious tourism', 'Architecture and heritage', 'Culture',
                'Gastronomy', 'Indigenous tourism', 'Museums and cultural centres', 'Relaxation', 'Sports', 'Theme parks']
    Mountain = ['Beach', 'Sports', 'Relaxation',
                'Water-based activities', 'Winter activities']
    Nature = ['Beach', 'Excitement', 'Sports', 'Water-based activities', 'Boat trips',
              'Museums and cultural centres', 'Nature', 'Relaxation', 'National parks and protected areas']
    Rural = ['Beach', 'Sports', 'Relaxation',
             'Rural', 'Water-based activities']
    Beach = ['Beach', 'Excitement', 'Sports',
             'Water-based activities', 'Boat trips', 'Nature', 'Relaxation']
    Urban = ['Architecture and heritage', 'Urban sightseeing', 'Arts', 'Beach', 'Sports', 'Culture',
             'Excitement', 'Nature', 'Relaxation', 'Museums and cultural centres', 'Theme parks']
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
        recommended_location_list = []

        for i in recommended_id_list:
            location = Location.query.filter_by(id=i).first()
            recommended_location_list.append(location.name)

        session['recommended_location_list'] = recommended_location_list
        # return render_template("recommendation.html", locations = recommended_location_list)
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
        return f"you haven't answer 1st question"


@app.route("/Q3", methods=["POST", "GET"])
@login_required
def Q3():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q3'))
        else:
            return redirect(url_for('Q4'))

    question = "In which state do you live?"
    answers = ['AC', 'AL', 'AP', 'AM', 'BA', 'CE', 'DF', 'ES', 'GO', 'MA', 'MT', 'MS', 'MG',
               'PA', 'PB', 'PR', 'PE', 'PI', 'RN', 'RS', 'RJ', 'RO', 'RR', 'SC', 'SP', 'SE', 'TO']
    return render_template('Q1.html', question=question, answers=answers)


# @app.route("/Q4", methods=["POST", "GET"])
# @login_required
# def Q4():
#     if request.method == 'POST':
#         answers = request.form.getlist('Q1')
#         if len(answers) != 1:
#             flash("You can only choose 1 option", 'danger')
#             return redirect(url_for('Q4'))
#         else:
#             return redirect(url_for('Q5'))

#     question = "In which municipality do you live?"
#     answers = []
#     return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q5", methods=["POST", "GET"])
@login_required
def Q5():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q5'))
        else:
            return redirect(url_for('Q6'))

    question = "Which mode of transport are you planning to use on your next trip?"
    answers = ['Road [within a 500km radius]', 'Air [+500km radius]']
    return render_template('yesorno.html', question=question, answers=answers)


@app.route("/Q6", methods=["POST", "GET"])
@login_required
def Q6():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q6'))
        else:
            if 'kid' in answers:
                return redirect(url_for('Q7'))
            # if there's no kid travelling, then skip Q7 and go straight to Q8
            else:
                return redirect(url_for('Q8'))

    question = "Who are you planning to travel with in your next trip?"
    answers = ['Couple', 'Couple with kids',
               'Adult friends / Relatives', 'A larger group with kids', 'Alone']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q7", methods=["POST", "GET"])
@login_required
def Q7():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q7'))
        else:
            return redirect(url_for('Q8'))

    question = "How old are the youngest kids in the travel party?"
    answers = ['0-2 years', '3-5 years', '6-11 years', '12-17 years']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q8", methods=["POST", "GET"])
@login_required
def Q8():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q8'))
        else:
            return redirect(url_for('Q9'))

    question = "How many days do you plan to stay away on your next trip?"
    answers = ['1-4 days', '5-10 days', '11+ days']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q9", methods=["POST", "GET"])
@login_required
def Q9():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q9'))
        else:
            return redirect(url_for('Q10'))

    question = "How much is your budget for this trip?"
    answers = ['Less than R$ 1,000',
               'R$ 1,000 to R$ 5,000', 'More than R$ 5,000']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q10", methods=["POST", "GET"])
@login_required
def Q10():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q10'))
        else:
            return redirect(url_for('Q11'))

    question = "What is your gender?"
    answers = ['Male', 'Female', 'Other / Prefer not to state']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q11", methods=["POST", "GET"])
@login_required
def Q11():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q11'))
        else:
            return redirect(url_for('Q12'))

    question = "What is your age?"
    answers = ['<10', '10-14', '15-20', '20-25',
               '25-30', '30-40', '40-50', '>50']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q12", methods=["POST", "GET"])
@login_required
def Q12():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q12'))
        else:
            return redirect(url_for('Q13'))

    question = "What is your highest level of education?"
    answers = ['No formal schooling', 'Elementary', 'High school',
               'Graduate', 'Postgraduate', 'Prefer not to say']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q13", methods=["POST", "GET"])
@login_required
def Q13():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q13'))
        else:
            return redirect(url_for('Q14'))

    question = "What is your current relationship status?"
    answers = ['Single', 'De facto', 'Married',
               'Divorced of Widowed', 'Prefer not to say']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q14", methods=["POST", "GET"])
@login_required
def Q14():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q14'))
        else:
            if 'Yes' in answers:
                return redirect(url_for('Q15'))
            # if there's no kid travelling, then skip Q15 and go straight to Q16
            else:
                return redirect(url_for('Q16'))

    question = "Do you have children?"
    answers = ['Yes', 'No']
    return render_template('yesorno.html', question=question, answers=answers)


@app.route("/Q15", methods=["POST", "GET"])
@login_required
def Q15():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q15'))
        else:
            return redirect(url_for('Q16'))

    question = "How old is your youngest kid?"
    answers = ['0-2 years', '3-5 years', '6-11 years', '12-17 years']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q16", methods=["POST", "GET"])
@login_required
def Q16():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q16'))
        else:
            return redirect(url_for('Q17'))

    question = "What is your household monthly income?"
    answers = ['R$ 0-500', 'R$ 500 - R$ 1000', 'R$ 1001 - R$ 2000',
               'R$ 2001 - R$ 4000', 'R$ 4001 - R$ 8000', 'R$ 8001+']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q17", methods=["POST", "GET"])
@login_required
def Q17():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q17'))
        else:
            return redirect(url_for('Q18'))

    question = "How many states in Brazil have you visited?"
    answers = ['Only my own state', '2-4 states', '5-10 states', '10+ states']
    return render_template('Q1.html', question=question, answers=answers)


@app.route("/Q18", methods=["POST", "GET"])
@login_required
def Q18():
    if request.method == 'POST':
        answers = request.form.getlist('Q1')
        if len(answers) != 1:
            flash("You can only choose 1 option", 'danger')
            return redirect(url_for('Q18'))
        else:
            return redirect(url_for('Q19'))

    question = "How many countries have you been to?"
    answers = ['Only Brazil', '2-4 countries',
               '5-10 countries', '10+ countries']
    return render_template('Q1.html', question=question, answers=answers)

# func to check if a string has a number


def has_numbers(inputString):
    return any(char.isdigit() for char in inputString)


@app.route("/Q19", methods=["POST", "GET"])
@login_required
def Q19():
    if request.method == 'POST':
        answers = request.form.getlist('QText')
        print(answers)
        if len(answers[0]) == 0:
            flash("Destination name must not be blank", 'danger')
            return redirect(url_for('Q19'))
        elif has_numbers(answers[0]):
            flash("Destination name must not have numbers", 'danger')
            return redirect(url_for('Q19'))
        else:
            recommended_location_list = session['recommended_location_list']
            return render_template("recommendation.html", locations=recommended_location_list)

    question = "Which was the best destination you have been to?"
    return render_template('QText.html', question=question)

# @app.route("/Q20", methods=["POST", "GET"])
# @login_required
# def Q20():
#     if request.method == 'POST':
#         answer = request.form.getlist('QPicture')
#         if len(answers) != 1 and session['times_looped'] != 3:
#             flash("You can only choose 1 option", 'danger')
#             return redirect(url_for('Q18'))
#         elif answer[0] == "Yes" and session['times_looped'] != 3:
#             session['times_looped'] += 1
#             return redirect(url_for('Q20'))
#         elif answer[0] == "No" and session['times_looped'] != 3:
#             session['times_looped'] += 1
#             return redirect(url_for('Q20'))
#         elif session['times_looped'] == 3:
#             return redirect(url_for('/'))

#     question = "Have you been to this destination?"
#     answers = ['Yes', 'No']
#     location =''
#     return render_template('QPicture.html', question = question, location = location, answers = answers)

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
