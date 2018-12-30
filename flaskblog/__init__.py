import os
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_bcrypt import Bcrypt
from flask_login import LoginManager
from flask_mail import Mail

app = Flask(__name__)
app.config['SECRET_KEY'] = '9b31b7cedaed4d5c79a672adb3bdfbbd'  # Some basic security measures apparently.
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///site.db'
db = SQLAlchemy(app)
bcrypt = Bcrypt(app)
login_manager = LoginManager(app)
login_manager.login_view = 'login'  # additional things the user can see when logged in
login_manager.login_message_category = 'info'
# app.config['MAIL_SERVER'] = 'smpt.googlemail.com'
# app.config['MAIL_PORT'] = 587
# app.config['MAIL_USE_TLS'] = True
# app.config['MAIL_USERNAME'] = os.environ.get('EMAIL_USER')
# app.config['MAIL_PASSWORD'] = os.environ.get('EMAIL_PASS')
# mail = Mail(app)
mail_settings = {"MAIL_SERVER": 'smtp.gmail.com',
                                "MAIL_PORT": 465,
                                "MAIL_USE_TLS": False,
                                "MAIL_USE_SSL": True,
                                "MAIL_USERNAME": os.environ['EMAIL_USER'],
                                "MAIL_PASSWORD": os.environ['EMAIL_PASSWORD']}  # This section is from youtube comments
app.config.update(mail_settings)
mail = Mail(app)

from flaskblog import routes  # Can't put this up top or it creates circular import logic
