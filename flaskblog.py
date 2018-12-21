from flask import Flask, render_template, url_for, flash, redirect
from forms import RegistrationForm, LoginForm
app = Flask(__name__)

app.config['SECRET_KEY'] = '9b31b7cedaed4d5c79a672adb3bdfbbd'  # Some basic security measures apparently.

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
    form = RegistrationForm()  # create the registration form
    if form.validate_on_submit():  # validate the user input upon submitting
        flash(f'Account created for {form.username.data}!', 'success')  # display a message for successful submit
        return redirect(url_for('home'))  # redirect the user after a successful submit
    return render_template('register.html', title='Register', form=form)


@app.route("/login", methods=['GET', 'POST'])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        if form.email.data == 'admin@blog.com' and form.password.data == 'password':  # test data. consider removing
            flash('You have been logged in!', 'success')  # test data. consider removing
            return redirect(url_for('home'))  # test data. consider removing
        else:  # test data. consider removing
            flash('Login Unsuccessful. Please check username and password', 'danger')  # test data. consider removing
    return render_template('login.html', title='Login', form=form)


if __name__ == '__main__':  # debug=True when we run the script directly. Lets us update the page w/o restarting webapp.
    app.run(debug=True)
