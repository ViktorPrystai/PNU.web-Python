from flask_wtf import FlaskForm
from wtforms import StringField, TextAreaField, SelectField, FileField, SubmitField
from wtforms.validators import DataRequired


class PostForm(FlaskForm):
    title = StringField('Title', validators=[DataRequired()])
    text = TextAreaField('Text', validators=[DataRequired()])
    image = FileField('Profile Image')
    type = SelectField('Type', choices=[('news', 'News'), ('publication', 'Publication'), ('other', 'Other')], validators=[DataRequired()])
    category = SelectField('Category', coerce=int)
    tags = StringField('Tags')
    submit = SubmitField('Submit')


class UpdateForm(FlaskForm):
    title = StringField('Title')
    text = TextAreaField('Text')
    image = FileField('Profile Image')
    type = SelectField('Type', choices=[('news', 'News'), ('publication', 'Publication'), ('other', 'Other')])
    category = SelectField('Category', coerce=int)
    tags = StringField('Tags')
    submit = SubmitField('Update')


class DeleteForm(FlaskForm):
    submit = SubmitField('Delete post')


class CategoryForm(FlaskForm):
    name = StringField('Name', validators=[DataRequired()])
    submit = SubmitField('Create Category')

class DeleteCategoryForm(FlaskForm):
    category_name = StringField('Category Name', validators=[DataRequired()])
    submit = SubmitField('Delete Category')