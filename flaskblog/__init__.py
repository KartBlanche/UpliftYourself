from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager


app = Flask(__name__)
app.config['SECRET_KEY'] = '9b31b7cedaed4d5c79a672adb3bdfbbd'  # Some basic security measures apparently.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # additional things the user can see when logged in
login_manager.login_message_category = 'info'


from flaskblog import routes  # Can't put this up top or it creates circular import logic
