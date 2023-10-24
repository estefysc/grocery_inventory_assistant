from flask_wtf import FlaskForm
from wtforms import IntegerField, SubmitField
from wtforms.validators import DataRequired, NumberRange

# This can be done as well to use StringField instead of IntegerField
# def validate_pin_range(form, field):
#     try:
#         pin_value = int(field.data)
#     except ValueError:
#         raise ValidationError("PIN must be a number.")

#     if pin_value < 1000 or pin_value > 9999:
#         raise ValidationError("PIN must be a 4-digit number.")

# class PinForm(FlaskForm):
#     pin = StringField('Enter PIN:', validators=[DataRequired(), validate_pin_range])
#     submit = SubmitField('Submit')

class PinForm(FlaskForm):
    pin = IntegerField('Enter PIN:', validators=[DataRequired(), NumberRange(min=1000, max=9999)])
    submit = SubmitField('Submit')