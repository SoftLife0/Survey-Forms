from flask_wtf import FlaskForm
from wtforms import StringField, SubmitField, SelectField
from wtforms.validators import DataRequired

class NewForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    description = StringField('Description', validators=[DataRequired()])
    consumer = StringField('Consumer')
    submit = SubmitField('Submit')


class NewQuestionForm(FlaskForm):
    text = StringField('Question Text', validators=[DataRequired()])
    response_type = SelectField('Response Type', choices=[('text', 'Text Input'), ('multiple_choice', 'Multiple Choice')], validators=[DataRequired()])
    submit = SubmitField('Add Question')