from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SubmitField
from wtforms.validators import DataRequired

class FeedbackForm(FlaskForm):
    name = StringField('Ім\'я', validators=[DataRequired()])
    message = TextAreaField('Відгук', validators=[DataRequired()])
    submit = SubmitField('Відправити')