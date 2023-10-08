from flask_wtf import FlaskForm
from wtforms import FileField, SubmitField
from wtforms.validators import ValidationError

# Define WTForm validators
def validate_file(form, field):
    if field.data is None or not field.data.filename.lower().endswith('.pdf'):
        raise ValidationError('Please upload a valid PDF file.')

# WTForm Class
class LeaseForm(FlaskForm):
    lease_file = FileField('Upload Lease Document', validators=[validate_file])
    submit = SubmitField('Analyze Lease')
