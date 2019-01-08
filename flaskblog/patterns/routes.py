from flask import render_template, Blueprint

patterns = Blueprint('patterns', __name__)


@patterns.route("/patterns")
def index():
    return render_template('patterns.html', title='Patterns')
