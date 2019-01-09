from flask import render_template, Blueprint, request

patterns = Blueprint('patterns', __name__)


@patterns.route("/patterns", methods=['GET', 'POST'])
@patterns.route("/patterns/index", methods=['GET', 'POST'])
def index():
    return render_template('patterns_index.html', title='Patterns Index')
