from flask_wtf import FlaskForm
from wtforms import StringField, IntegerField, SubmitField, PasswordField
from wtforms.validators import DataRequired

class LoginForm(FlaskForm):
    employee_code = StringField("Employee Code", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")

class DemandForm(FlaskForm):
    sugar_kg = IntegerField("Sugar (kg)", validators=[DataRequired()])
    oil_kg = IntegerField("Oil (kg)", validators=[DataRequired()])
    submit = SubmitField("Submit Demand")