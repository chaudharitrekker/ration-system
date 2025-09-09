from app import db
from datetime import datetime

class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_sugar = db.Column(db.Integer, nullable=False, default=0)
    requested_oil = db.Column(db.Integer, nullable=False, default=0)
    approved_sugar = db.Column(db.Integer, nullable=True)
    approved_oil = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="Pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    employee_code = db.Column(db.String(50), nullable=False)


