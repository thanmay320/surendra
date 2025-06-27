from flask_wtf import FlaskForm
from wtforms import StringField, FloatField, TextAreaField, SubmitField, FileField, MultipleFileField
from wtforms.validators import DataRequired, Length
from flask_wtf.file import FileAllowed, FileRequired


class ProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=2, max=150)])
    project_description = TextAreaField('Description')
    project_price = FloatField('Price', validators=[DataRequired()])
    project_technologies = StringField('Technologies Used', validators=[DataRequired()])

    project_thumbnail = FileField('Thumbnail (Image)', validators=[
        FileRequired(), FileAllowed(['jpg', 'png', 'jpeg'], 'Images only!')
    ])

    images = MultipleFileField('Additional Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png'], 'Only images are allowed')
    ])

    project_files = MultipleFileField('Project Files', validators=[
        FileAllowed(['pdf', 'zip', 'docx', 'txt'], 'Invalid file type')
    ])

    submit = SubmitField('Create Project')
