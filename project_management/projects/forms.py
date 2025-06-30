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
        FileRequired(), FileAllowed(['jpg', 'png', 'jpeg','webp'], 'Images only!')
    ])

    images = MultipleFileField('Additional Images', validators=[
        FileAllowed(['jpg', 'jpeg', 'png','webp'], 'Only images are allowed')
    ])

    project_files = MultipleFileField('Project Files', validators=[
        FileAllowed(['pdf', 'zip', 'docx', 'txt'], 'Invalid file type')
    ])

    submit = SubmitField('Create Project')


class EditProjectForm(FlaskForm):
    project_name = StringField('Project Name', validators=[DataRequired(), Length(min=3, max=100)])
    project_description = TextAreaField('Project Description', validators=[DataRequired(), Length(min=10)])
    project_price = FloatField('Project Price (₹)', validators=[DataRequired()])
    project_technologies = StringField('Technologies (comma-separated)', validators=[DataRequired()])

    project_thumbnail = FileField('Project Thumbnail (JPG/PNG only)', validators=[FileAllowed(['jpg', 'jpeg', 'png','webp'])])
    gallery_images = FileField('Add Gallery Images (Multiple JPG/PNG)', render_kw={"multiple": True},
                               validators=[FileAllowed(['jpg', 'jpeg', 'png','webp'])])
    project_files = FileField('Add Project Files (ZIP/PDF)', render_kw={"multiple": True},
                              validators=[FileAllowed(['zip', 'pdf'])])

    submit = SubmitField('Update Project')
