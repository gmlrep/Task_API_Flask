from flask_wtf import FlaskForm
from wtforms import StringField
from wtforms.validators import DataRequired


class TaskAAddForm(FlaskForm):
    title = StringField('title', validators=[DataRequired()])
    description = StringField('description', validators=[DataRequired()])


class TaskUpdateForm(FlaskForm):
    title = StringField('title')
    description = StringField('description')



