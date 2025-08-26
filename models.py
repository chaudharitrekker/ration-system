#from extensions import db
#from datetime import datetime
from app import db
from datetime import datetime

class Employee(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    ration_id = db.Column(db.String(50), unique=True, nullable=False)
    name = db.Column(db.String(100), nullable=False)
    contact_no = db.Column(db.String(15), nullable=False)
    address = db.Column(db.Text, nullable=False)
    status = db.Column(db.String(20), default="Pending")   
    demands = db.relationship('Demand', backref='employee', lazy=True)

    def __repr__(self):
        return f"<Employee {self.name}>"

class Demand(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    requested_sugar = db.Column(db.Integer, nullable=False, default=0)
    requested_oil = db.Column(db.Integer, nullable=False, default=0)
    approved_sugar = db.Column(db.Integer, nullable=True)
    approved_oil = db.Column(db.Integer, nullable=True)
    status = db.Column(db.String(20), default="Pending")
    date_created = db.Column(db.DateTime, default=datetime.utcnow)
    employee_id = db.Column(db.Integer, db.ForeignKey("employee.id"), nullable=False)


