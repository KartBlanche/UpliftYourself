from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, TextAreaField, IntegerField
from wtforms.validators import DataRequired


class PatternForm(FlaskForm):
    id = IntegerField('ID (used to sort in Index)', validators=[DataRequired()])
    title = StringField('Title (primary key and URL)', validators=[DataRequired()])
    content = TextAreaField('Pattern Summary')
    submit = SubmitField('Create/Update Pattern')


class SectionForm(FlaskForm):
    title = StringField('Section Title', validators=[DataRequired()])
    content = TextAreaField('Content', validators=[DataRequired()])
    submit = SubmitField('Create/Update Pattern Section')
