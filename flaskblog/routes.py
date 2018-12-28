from flask import render_template, url_for, flash, redirect, request
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required

posts = [  # test data. consider removing
    {
        'author': 'Corey Schafer',  # test data. consider removing
        'title': 'Blog Post 1',  # test data. consider removing
        'content': 'First post content',  # test data. consider removing
        'date_posted': 'April 20, 2018'  # test data. consider removing
    },
    {
        'author': 'Jane Doe',  # test data. consider removing
        'title': 'Blog Post 2',  # test data. consider removing
        'content': 'Second post content',  # test data. consider removing
        'date_posted': 'April 21, 2018'  # test data. consider removing
    }
]  # test data. consider removing


@app.route("/")
@app.route("/home")  # Each successive @app.route is a different way to get to the same page.
def home():  # Each @app.route above uses this same function.
    return render_template('home.html', posts=posts)  # returns the html code from the home.html file


@app.route("/about")
def about():
    return render_template('about.html', title='About')


@app.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if the user is logged in and tries to log in, redirect home
        return redirect(url_for('home'))
    form = RegistrationForm()  # create the registration form
    if form.validate_on_submit():  # validate the user input upon submitting
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')  # hash the user password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # create this user
        db.session.add(user)  # prepare to add this user to the db
        db.session.commit()  # commit/add this user to the db
        flash(f'Account created for {form.username.data}!', 'success')  # display a message for successful submit
        return redirect(url_for('login'))  # redirect the user after a successful submit
    return render_template('register.html', title='Register', form=form)  # here's the register template


@app.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if the user is logged in and tries to register, redirect home
        return redirect(url_for('home'))
    form = LoginForm()  # create the login form
    if form.validate_on_submit():  # validate the user input upon submitting
        user = User.query.filter_by(email=form.email.data).first()  # get the info of the user with that email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # compare the passwords
            login_user(user, remember=form.remember.data)  # log in user and check if they wanted to be remembered
            next_page = request.args.get('next')  # if they needed to log in to view a page, redirect after log in
            return redirect(next_page) if next_page else redirect(url_for('home'))  # upon success, send them home
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')  # upon failure, flash this message
    return render_template('login.html', title='Login', form=form)  # here's the login template


@app.route("/logout")
def logout():
    logout_user()
    return redirect(url_for('home'))


@app.route("/account")
@login_required
def account():
    return render_template('account.html', title='Account')
