from flask_wtf import FlaskForm
from wtforms import StringField, SelectField, TextAreaField, DateField, FileField, SubmitField, IntegerField, PasswordField
from wtforms.validators import DataRequired, Length, Optional

def load_units():
    """Load units list from units.txt file"""
    try:
        with open("units.txt") as f:
            return [(line.strip(), line.strip()) for line in f if line.strip()]
    except FileNotFoundError:
        # fallback agar file missing ho
        return [("Default Unit", "Default Unit")]

class LoginForm(FlaskForm):
    username = StringField("Username", validators=[DataRequired()])
    password = PasswordField("Password", validators=[DataRequired()])
    submit = SubmitField("Login")


class DemandForm(FlaskForm):
    sugar_kg = IntegerField("Sugar (kg)", validators=[DataRequired()])
    oil_kg = IntegerField("Oil (kg)", validators=[DataRequired()])
    submit = SubmitField("Submit Demand")

class OfficerDemandForm(FlaskForm):
    name = StringField("Name", validators=[DataRequired(), Length(max=100)])
    rank = StringField("Rank", validators=[DataRequired(), Length(max=50)])
    employee_number = StringField("P.No", validators=[DataRequired(), Length(max=20)])

    ration_type = SelectField("Ration Type", choices=[("PV","PV"),("EV","EV"),("S","S")], validators=[DataRequired()])
    address = TextAreaField("Residential Address", validators=[DataRequired()])
    unit = SelectField("Unit", choices=[], validators=[DataRequired()])  # populate dynamically
    office_phone = StringField("Office 5-digit", validators=[DataRequired(), Length(max=5)])
    mobile = StringField("Mobile No", validators=[DataRequired(), Length(max=15)])
    collection_type = SelectField(
        "Collection Type",
        choices=[("SELF","SELF (Rs.120)"), ("HOME_DELIVERY","HOME DELIVERY (Rs.150)"), ("HON_OFFICER","HON. OFFICER (Rs.70)")],
        validators=[DataRequired()]
    )
    bank_account = StringField("Bank Account Number", validators=[DataRequired()])
    ifsc = StringField("IFSC Code", validators=[DataRequired()])
    
    rik_gx_number = StringField("RIK Commencement GX Number", validators=[DataRequired()])
    rik_gx_date = DateField("RIK Commencement Date", validators=[DataRequired()])
    rik_gx_file = FileField("Upload GX Form")  # File allowed: pdf/image
    
    retirement_date = DateField("Date of Retirement (Hon. Officer)", validators=[])
    promotion_gx_number = StringField("Promotion GX Number (Hon. Officer)")
    promotion_gx_date = DateField("Promotion GX Date")

    submit = SubmitField("Submit")
