from datetime import datetime
from app import db
from werkzeug.security import generate_password_hash, check_password_hash

class User(db.Model):
    __tablename__ = "users"   # avoid reserved keyword "user"

    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(50), unique=True, nullable=False)
    password_hash = db.Column(db.String(256), nullable=False)  # increased length
    role = db.Column(db.String(20), nullable=False)  # "admin" or "delivery"

    def set_password(self, password):
        self.password_hash = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password_hash, password)
        
class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_sugar = db.Column(db.Integer, nullable=False, default=0)
    requested_oil = db.Column(db.Integer, nullable=False, default=0)
    approved_sugar = db.Column(db.Integer, nullable=True)
    approved_oil = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="Pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    employee_code = db.Column(db.String(50), nullable=False)


class OfficerDemand(db.Model):
    __tablename__ = "officer_demands"

    id = db.Column(db.Integer, primary_key=True)
    employee_number = db.Column(db.String(50), nullable=False)
    name = db.Column(db.String(100), nullable=False)
    rank = db.Column(db.String(50), nullable=False)
    ration_type = db.Column(db.String(10), nullable=False)
    address = db.Column(db.Text, nullable=False)
    unit = db.Column(db.String(100), nullable=False)
    office_phone = db.Column(db.String(10), nullable=False)
    mobile = db.Column(db.String(15), nullable=False)
    collection_type = db.Column(db.String(50), nullable=False)
    bank_account = db.Column(db.String(30), nullable=False)
    ifsc = db.Column(db.String(20), nullable=False)
    rik_gx_number = db.Column(db.String(50), nullable=False)
    rik_gx_date = db.Column(db.Date, nullable=False)
    rik_gx_file = db.Column(db.String(200))
    retirement_date = db.Column(db.Date, nullable=True)
    promotion_gx_number = db.Column(db.String(50), nullable=True)
    promotion_gx_date = db.Column(db.Date, nullable=True)
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    status = db.Column(db.String(20), default="Pending")

    # new columns for 1st and 2nd half of month
    availability_first15 = db.Column(db.Integer, nullable=True)
    availability_second15 = db.Column(db.Integer, nullable=True)

    created_by = db.Column(db.String(20))

    @property
    def availability_total(self):
        return (self.availability_first15 or 0) + (self.availability_second15 or 0)

class RaisedDemand(db.Model):
    __tablename__ = "raised_demands"

    id = db.Column(db.Integer, primary_key=True)
    officer_demand_id = db.Column(db.Integer, db.ForeignKey("officer_demands.id"), nullable=False)
    raiser_id = db.Column(db.String(50), nullable=False)  # who raised demand
    demand_type = db.Column(db.String(20), nullable=False)  # 'first15' / 'second15' / 'dry'
    availability_days = db.Column(db.Integer, nullable=True)  # manual input
    status = db.Column(db.String(20), default="ToBeIssued")  # 'ToBeIssued' / 'Issued'
    date_created = db.Column(db.DateTime, default=datetime.utcnow)

    officer = db.relationship("OfficerDemand", backref="raised_demands")


