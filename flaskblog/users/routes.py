from flask import render_template, url_for, flash, redirect, request, Blueprint
from flask_login import login_user, current_user, logout_user, login_required
from flaskblog import db, bcrypt
from flaskblog.models import User, Post
from flaskblog.users.forms import (RegistrationForm, LoginForm, UpdateAccountForm,
                                   RequestResetForm, ResetPasswordForm)
from flaskblog.users.utils import save_picture, send_reset_email

users = Blueprint('users', __name__)


@users.route("/register", methods=['GET', 'POST'])
def register():
    if current_user.is_authenticated:  # if the user is logged in and tries to log in, redirect home
        return redirect(url_for('main.home'))
    form = RegistrationForm()  # create the registration form
    if form.validate_on_submit():  # validate the user input upon submitting
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')  # hash the user password
        user = User(username=form.username.data, email=form.email.data, password=hashed_password)  # create this user
        db.session.add(user)  # prepare to add this user to the db
        db.session.commit()  # commit/add this user to the db
        flash(f'Account created for {form.username.data}!', 'success')  # display a message for successful submit
        return redirect(url_for('users.login'))  # redirect the user after a successful submit
    return render_template('register.html', title='Register', form=form)  # here's the register template


@users.route("/login", methods=['GET', 'POST'])
def login():
    if current_user.is_authenticated:  # if the user is logged in and tries to register, redirect home
        return redirect(url_for('main.home'))
    form = LoginForm()  # create the login form
    if form.validate_on_submit():  # validate the user input upon submitting
        user = User.query.filter_by(email=form.email.data).first()  # get the info of the user with that email
        if user and bcrypt.check_password_hash(user.password, form.password.data):  # compare the passwords
            login_user(user, remember=form.remember.data)  # log in user and check if they wanted to be remembered
            next_page = request.args.get('next')  # if they needed to log in to view a page, redirect after log in
            return redirect(next_page) if next_page else redirect(url_for('main.home'))  # upon success, send them home
        else:
            flash('Login Unsuccessful. Please check email and password.', 'danger')  # upon failure, flash this message
    return render_template('login.html', title='Login', form=form)  # here's the login template


@users.route("/logout")  # let the user log out
def logout():
    logout_user()
    return redirect(url_for('main.home'))


@users.route("/account", methods=['GET', 'POST'])
@login_required
def account():
    form = UpdateAccountForm()
    if form.validate_on_submit():  # this section lets the user update their picture, username, and email
        if form.picture.data:
            picture_file = save_picture(form.picture.data)
            current_user.image_file = picture_file
        current_user.username = form.username.data
        current_user.email = form.email.data
        db.session.commit()
        flash('Your account has been updated!', 'success')
        return redirect(url_for('users.account'))
    elif request.method == 'GET':  # this section auto populates the username and email forms
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # show the user's profile pic
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@users.route("/user/<string:username>")
def user_posts(username):
    page = request.args.get('page', 1, type=int)
    user = User.query.filter_by(username=username).first_or_404()
    posts = Post.query.filter_by(author=user)\
        .order_by(Post.date_posted.desc())\
        .paginate(page=page, per_page=5)  # filter by author, descending order, 5 per page
    return render_template('user_posts.html', posts=posts, user=user)


@users.route("/reset_password", methods=['GET', 'POST'])
def reset_request():
    if current_user.is_authenticated:  # if the user is logged in and tries to reset password, redirect home
        return redirect(url_for('main.home'))
    form = RequestResetForm()
    if form.validate_on_submit():
        user = User.query.filter_by(email=form.email.data).first()
        send_reset_email(user)
        flash('An email has been sent with instructions to reset your password.', 'info')
        return redirect(url_for('users.login'))
    return render_template('reset_request.html', title='Reset Password', form=form)


@users.route("/reset_password/<token>", methods=['GET', 'POST'])
def reset_token(token):
    if current_user.is_authenticated:  # if the user is logged in and tries to reset password, redirect home
        return redirect(url_for('main.home'))
    user = User.verify_reset_token(token)
    if user is None:
        flash('That is an invalid or expired token.', 'warning')
        return redirect(url_for('users.reset_request'))
    form = ResetPasswordForm()
    if form.validate_on_submit():  # validate the user input upon submitting
        hashed_password = bcrypt.generate_password_hash(form.password.data).decode('UTF-8')  # hash the user password
        user.password = hashed_password
        db.session.commit()  # commit this new password to the database
        flash(f'Your password has been updated!', 'success')  # display a message for successful submit
        return redirect(url_for('users.login'))  # redirect the user after a successful submit
    return render_template('reset_token.html', title='Reset Password', form=form)
