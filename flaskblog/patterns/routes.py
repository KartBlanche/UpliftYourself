from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Pattern
from flaskblog.patterns.forms import PatternForm

patterns = Blueprint('patterns', __name__)


@patterns.route("/patterns/index")
@patterns.route("/patterns")
def index():
    return render_template('patterns_index.html', title='Patterns Index')


@patterns.route("/patterns/new", methods=['GET', 'POST'])
@login_required
def new_pattern():  # let the user make patterns when logged in
    form = PatternForm()
    if form.validate_on_submit():
        pattern = Pattern(title=form.title.data, content=form.content.data)
        db.session.add(pattern)
        db.session.commit()
        flash('Your pattern has been created!', 'success')
        return redirect(url_for('patterns.index'))
    return render_template('create_post.html', title='New Pattern', form=form, legend='New Pattern')


@patterns.route("/patterns/<int:pattern_id>")
def pattern(pattern_id):  # make an individual page for each post, distinguished by post_id
    pattern = Pattern.query.get_or_404(pattern_id)
    return render_template('pattern.html', title=pattern.title, post=pattern)


@patterns.route("/patterns/<int:pattern_id>/update", methods=['GET', 'POST'])
@login_required
def update_pattern(pattern_id):  # let admins update patterns
    pattern = Pattern.query.get_or_404(pattern_id)
    if pattern.author != current_user:  # only the pattern owner can update it
        abort(403)
    form = PatternForm()
    if form.validate_on_submit():  # update the pattern in the database
        pattern.title = form.title.data
        pattern.content = form.content.data
        db.session.commit()
        flash('Your pattern has been updated!', 'success')
        return redirect(url_for('patterns.pattern', pattern_id=pattern.id))
    elif request.method == 'GET':  # auto populate forms with the existing pattern info
        form.title.data = pattern.title
        form.content.data = pattern.content
    return render_template('create_post.html', title='Update Pattern', form=form, legend='Update Pattern')


@patterns.route("/patterns/<int:pattern_id>/delete", methods=['POST'])
@login_required
def delete_pattern(pattern_id):  # let users delete their patterns
    pattern = Pattern.query.get_or_404(pattern_id)
    if pattern.author != current_user:  # only the pattern owner can delete it
        abort(403)
    db.session.delete(pattern)
    db.session.commit()
    flash('Your pattern has been deleted.', 'success')
    return redirect(url_for('patterns.index'))
