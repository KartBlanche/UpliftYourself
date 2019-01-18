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
    patterns_list = Pattern.query.order_by(Pattern.id.asc()) \
        .paginate(page=page, per_page=10)
    return render_template('patterns_index.html', patterns_list=patterns_list)


@patterns.route("/patterns/new", methods=['GET', 'POST'])
@login_required
def new_pattern():  # let the user make patterns when logged in
    form = PatternForm()
    if form.validate_on_submit():
        pattern = Pattern(id=form.id.data, title=form.title.data, content=form.content.data)
        db.session.add(pattern)
        db.session.commit()
        flash('Your pattern has been created!', 'success')
        return redirect(url_for('patterns.index'))
    return render_template('create_pattern.html', title='New Pattern', form=form, legend='New Pattern')


@patterns.route("/patterns/<string:title>/new", methods=['GET', 'POST'])
@login_required
def new_section(title):  # let the user make patterns when logged in
    if current_user.role != 'admin':  # only admins can update
        abort(403)
    form = SectionForm()
    if form.validate_on_submit():
        section = Section(title=form.title.data, content=form.content.data, pattern_title=title)
        db.session.add(section)
        db.session.commit()
        flash('Your pattern section has been created!', 'success')
        return redirect(url_for('patterns.index'))
    return render_template('create_post.html', title='New Section', form=form, legend='New Section')


@patterns.route("/patterns/<string:title>/<int:section_id>")
def section(section_id):  # make an individual page for each section, distinguished by section_id
    section = Section.query.get_or_404(section_id)
    return render_template('pattern_section.html', title=section.title, section=section)


@patterns.route("/patterns/<string:title>")
def pattern(title):
    page = request.args.get('page', 1, type=int)
    pattern = Pattern.query.filter_by(title=title).first_or_404()
    sections = Section.query.filter_by(parent_pattern=pattern) \
        .order_by(Section.id.asc()) \
        .paginate(page=page, per_page=10)
    return render_template('pattern.html', sections=sections, pattern=pattern)


@patterns.route("/patterns/<string:title>/<int:section_id>/update", methods=['GET', 'POST'])
@login_required
def update_section(title, section_id):  # let admins update pattern sections
    pattern = Pattern.query.get_or_404(title)
    section = Section.query.get_or_404(section_id)
    if current_user.role != 'admin':  # only admins can update
        abort(403)
    form = SectionForm()
    if form.validate_on_submit():  # update the pattern section in the database
        section.title = form.title.data
        section.content = form.content.data
        db.session.commit()
        flash('Your pattern section has been updated!', 'success')
        return redirect(url_for('patterns.index', title=pattern.title, section_id=section.id))
    elif request.method == 'GET':  # auto populate forms with the existing pattern section info
        form.title.data = section.title
        form.content.data = section.content
    return render_template('create_post.html', title='Update Pattern Section', form=form, legend='Update Section')


@patterns.route("/patterns/<string:title>/update", methods=['GET', 'POST'])
@login_required
def update_pattern(title):  # let admins update pattern sections
    pattern = Pattern.query.get_or_404(title)
    if current_user.role != 'admin':  # only admins can update
        abort(403)
    form = PatternForm()
    if form.validate_on_submit():  # update the pattern section in the database
        pattern.id = form.id.data
        pattern.title = form.title.data
        pattern.content = form.content.data
        db.session.commit()
        flash('Your pattern has been updated!', 'success')
        return redirect(url_for('patterns.index', pattern_title=pattern.title))
    elif request.method == 'GET':  # auto populate forms with the existing pattern section info
        form.id.data = pattern.id
        form.title.data = pattern.title
        form.content.data = pattern.content
    return render_template('create_pattern.html', title='Update Pattern', form=form, legend='Update Pattern')


@patterns.route("/patterns/sections/<int:section_id>/delete", methods=['POST'])
@login_required
def delete_section(section_id):  # let users delete their posts
    section = Section.query.get_or_404(section_id)
    if current_user.role != 'admin':  # only the post owner can delete it
        abort(403)
    db.session.delete(section)
    db.session.commit()
    flash('Your pattern section has been deleted.', 'success')
    return redirect(url_for('patterns.index'))


@patterns.route("/patterns/<string:title>/delete", methods=['POST'])
@login_required
def delete_pattern(title):  # let users delete their posts
    pattern = Pattern.query.get_or_404(title)
    sections = Section.query.filter_by(parent_pattern=pattern) \
        .order_by(Section.id.asc())
    if current_user.role != 'admin':  # only the post owner can delete it
        abort(403)
    for section in sections:
        db.session.delete(section)
    db.session.delete(pattern)
    db.session.commit()
    flash('Your pattern has been deleted.', 'success')
    return redirect(url_for('patterns.index'))
