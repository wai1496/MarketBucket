from flask_wtf import FlaskForm
from flask_wtf.csrf import CsrfProtect
from wtforms import FileField, PasswordField, SubmitField, TextAreaField


class UploadForm(FlaskForm):
    user_image = FileField('User Image')
    image_caption = TextAreaField('Image Caption')
    submit = SubmitField('Submit')


class EditCaptionForm(FlaskForm):
    image_caption = TextAreaField('Image Caption')
    submit = SubmitField('Submit')


class DeleteForm(FlaskForm):
    submit = SubmitField('Submit')
