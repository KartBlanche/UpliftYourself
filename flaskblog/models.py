from datetime import datetime
from itsdangerous import TimedJSONWebSignatureSerializer as Serializer
from flask import current_app
from flaskblog import db, login_manager, admin
from flask_login import UserMixin
from flask_admin.contrib.sqla import ModelView


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(20), unique=True, nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    image_file = db.Column(db.String(20), nullable=False, default='default.jpg')
    password = db.Column(db.String(60), nullable=False)
    posts = db.relationship('Post', backref='author', lazy=True)
    role = db.Column(db.String(20), default='user')

    def get_reset_token(self, expires_sec=1800):  # expiration time
        s = Serializer(current_app.config['SECRET_KEY'], expires_sec)
        return s.dumps({'user_id': self.id}).decode('utf-8')  # create a token with a payload of the user_id

    @staticmethod  # don't expect a self parameter. just expect token
    def verify_reset_token(token):
        s = Serializer(current_app.config['SECRET_KEY'])  # create a serializer with a token
        try:
            user_id = s.loads(token)['user_id']  # try to load the token
        except:
            return None
        return User.query.get(user_id)  # if no exception, return user_id

    def __repr__(self):
        return f"User('{self.username}', '{self.email}', '{self.image_file}')"


class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    date_posted = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    content = db.Column(db.Text, nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)

    def __repr__(self):
        return f"Post('{self.title}', '{self.date_posted}')"


class Pattern(db.Model):
    id = db.Column(db.Integer, unique=True, nullable=False)
    title = db.Column(db.String(100), primary_key=True, unique=True, nullable=False)
    content = db.Column(db.Text)
    sections = db.relationship('Section', backref='parent_pattern', lazy=True)

    def __repr__(self):
        return f"Pattern('{self.id}', '{self.title}')"


class Section(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(100), nullable=False)
    content = db.Column(db.Text, nullable=False)
    pattern_title = db.Column(db.Integer, db.ForeignKey('pattern.title'), nullable=False)

    def __repr__(self):
        return f"Section('{self.id}', '{self.title}')"


admin.add_view(ModelView(User, db.session))
admin.add_view(ModelView(Post, db.session))
admin.add_view(ModelView(Pattern, db.session))


