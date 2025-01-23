from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import DataRequired
from werkzeug.utils import secure_filename

class GeoJSONUploadForm(FlaskForm):
    file = FileField('Upload GeoJSON File', validators=[DataRequired()])
    submit = SubmitField('Upload')
