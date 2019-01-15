from flask import (render_template, url_for, flash,
                   redirect, request, abort, Blueprint)
from flask_login import current_user, login_required
from flaskblog import db
from flaskblog.models import Pattern, Section
from flaskblog.patterns.forms import PatternForm, SectionForm

patterns = Blueprint('patterns', __name__)


@patterns.route("/patterns/index")
@patterns.route("/patterns")
def index():
    page = request.args.get('page', 1, type=int)
    patterns_list = Pattern.query.order_by(Pattern.id.asc())\
        .paginate(page=page, per_page=10)
    return render_template('patterns_index.html', patterns_list=patterns_list)


@patterns.route("/patterns/new", methods=['GET', 'POST'])
@login_required
def new_pattern():  # let the user make patterns when logged in
    form = PatternForm()
    if form.validate_on_submit():
        pattern = Pattern(title=form.title.data)
        db.session.add(pattern)
        db.session.commit()
        flash('Your pattern has been created!', 'success')
        return redirect(url_for('patterns.index'))
    return render_template('create_post.html', title='New Pattern', form=form, legend='New Pattern')


@patterns.route("/patterns/<int:section_id>")
def section(section_id):  # make an individual page for each section, distinguished by section_id
    section = Section.query.get_or_404(section_id)
    return render_template('pattern_section.html', title=section.title, section=section)


@patterns.route("/patterns/<string:title>")
def pattern(title):
    page = request.args.get('page', 1, type=int)
    pattern = Pattern.query.filter_by(title=title).first_or_404()
    sections = Section.query.filter_by(parent_pattern=pattern)\
        .order_by(Section.id.asc()) \
        .paginate(page=page, per_page=10)
    return render_template('pattern.html', sections=sections, pattern=pattern)


@patterns.route("/patterns/<int:section_id>/update", methods=['GET', 'POST'])
@login_required
def update_section(section_id):  # let admins update pattern sections
    section = Section.query.get_or_404(section_id)
    if current_user.role != 'admin':  # only admins can update
        abort(403)
    form = SectionForm()
    if form.validate_on_submit():  # update the pattern section in the database
        section.title = form.title.data
        section.content = form.content.data
        db.session.commit()
        flash('Your pattern section has been updated!', 'success')
        return redirect(url_for('patterns.index', section_id=section.id))
    elif request.method == 'GET':  # auto populate forms with the existing pattern section info
        form.title.data = section.title
        form.content.data = section.content
    return render_template('create_post.html', title='Update Pattern Section', form=form, legend='Update Section')

