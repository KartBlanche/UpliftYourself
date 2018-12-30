import os
import secrets
from PIL import Image
from flask import render_template, url_for, flash, redirect, request, abort
from flaskblog import app, db, bcrypt
from flaskblog.forms import RegistrationForm, LoginForm, UpdateAccountForm, PostForm
from flaskblog.models import User, Post
from flask_login import login_user, current_user, logout_user, login_required


@app.route("/")
@app.route("/home")  # Each successive @app.route is a different way to get to the same page.
def home():  # Each @app.route above uses this same function.
    posts = Post.query.all()
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


@app.route("/logout")  # let the user log out
def logout():
    logout_user()
    return redirect(url_for('home'))


def save_picture(form_picture):  # save the picture to our picture folder as a random hex
    random_hex = secrets.token_hex(8)
    _, f_ext = os.path.splitext(form_picture.filename)
    picture_fn = random_hex + f_ext
    picture_path = os.path.join(app.root_path, 'static/profile_pics', picture_fn)

    output_size = (125, 125)  # resize the image before saving
    i = Image.open(form_picture)
    i.thumbnail(output_size)
    i.save(picture_path)

    return picture_fn


@app.route("/account", methods=['GET', 'POST'])
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
        return redirect(url_for('account'))
    elif request.method == 'GET':  # this section auto populates the username and email forms
        form.username.data = current_user.username
        form.email.data = current_user.email
    image_file = url_for('static', filename='profile_pics/' + current_user.image_file)  # show the user's profile pic
    return render_template('account.html', title='Account', image_file=image_file, form=form)


@app.route("/post/new", methods=['GET', 'POST'])
@login_required
def new_post():
    form = PostForm()
    if form.validate_on_submit():
        post = Post(title=form.title.data, content=form.content.data, author=current_user)
        db.session.add(post)
        db.session.commit()
        flash('Your post has been created!', 'success')
        return redirect(url_for('home'))
    return render_template('create_post.html', title='New Post', form=form, legend='New Post')


@app.route("/post/<int:post_id>")
def post(post_id):
    post = Post.query.get_or_404(post_id)
    return render_template('post.html', title=post.title, post=post)


@app.route("/post/<int:post_id>/update", methods=['GET', 'POST'])
@login_required
def update_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    form = PostForm()
    if form.validate_on_submit():
        post.title = form.title.data
        post.content = form.content.data
        db.session.commit()
        flash('Your post has been updated!', 'success')
        return redirect(url_for('post', post_id=post.id))
    elif request.method == 'GET':
        form.title.data = post.title
        form.content.data = post.content
    return render_template('create_post.html', title='Update Post', form=form, legend='Update Post')


@app.route("/post/<int:post_id>/delete", methods=['POST'])
@login_required
def delete_post(post_id):
    post = Post.query.get_or_404(post_id)
    if post.author != current_user:
        abort(403)
    db.session.delete(post)
    db.session.commit()
    flash('Your post has been deleted.', 'success')
    return redirect(url_for('home'))

