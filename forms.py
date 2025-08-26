from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField
from wtforms.validators import DataRequired

class RegistrationForm(FlaskForm):
    #ration_id = StringField("Ration ID", validators=[DataRequired()])
    name = StringField("Name", validators=[DataRequired()])
    contact_no = StringField("Contact No", validators=[DataRequired()])
    address = StringField("Address", validators=[DataRequired()])
    submit = SubmitField("Register")

class DemandForm(FlaskForm):
    sugar_kg = IntegerField("Sugar (kg)", validators=[DataRequired()])
    oil_kg = IntegerField("Oil (kg)", validators=[DataRequired()])
    submit = SubmitField("Submit Demand")
