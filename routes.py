from flask import Flask, render_template, request, redirect, url_for, flash , session 
from app import app, db
from models import Employee, Demand
from forms import RegistrationForm, DemandForm

app.secret_key = "super_secret_key"

@app.route("/")
def home():
    employees = Employee.query.all()
    return render_template("home.html", employees=employees)

@app.route("/register", methods=["GET", "POST"])
def register():
    form = RegistrationForm()
    if form.validate_on_submit():
        ration_id = generate_ration_id()
        new_emp = Employee(
            ration_id=ration_id,
            name=form.name.data,
            contact_no=form.contact_no.data,
            address=form.address.data,
            status="Pending"
        )
        db.session.add(new_emp)
        db.session.commit()
        return f"""
        ✅ Registration successful! Your Ration ID is {ration_id}. Please wait for admin approval. 
        <br><br>
        <a href='{url_for('home')}'>⬅️ Back to Home page</a>
        """
        #return f"✅ Registration successful! Your Ration ID is {ration_id}. Please wait for admin approval."
    return render_template("register.html", form=form)

def generate_ration_id():
    last_emp = Employee.query.order_by(Employee.id.desc()).first()
    if last_emp and last_emp.ration_id:
        last_num = int(last_emp.ration_id.replace("RAT", ""))
        new_num = last_num + 1
    else:
        new_num = 1001
    return f"RAT{new_num}"

   
@app.route("/demand", methods=["GET", "POST"])
def demand():
    form = DemandForm()
    if form.validate_on_submit():
        ration_id = request.form.get("ration_id")
        employee = Employee.query.filter_by(ration_id=ration_id).first()

        if not employee:
            return render_template("message.html", message="❌ Invalid Ration ID. Please register first.")

        if employee.status != "Active":
            return render_template("message.html", message=f"⚠️ Your registration status is {employee.status}. You cannot place a demand.")

        new_demand = Demand(
            requested_sugar=form.sugar_kg.data,
            requested_oil=form.oil_kg.data,
            employee_id=employee.id
        )
        db.session.add(new_demand)
        db.session.commit()
        return render_template("message.html", message="✅ Demand placed successfully! Wait for admin approval.")
        
    return render_template("demand.html", form=form)

@app.route("/approve_demand/<int:demand_id>", methods=["POST"])
def approve_demand(demand_id):
    demand = Demand.query.get_or_404(demand_id)

    # get approved values from form
    approved_sugar = int(request.form.get("approved_sugar", 0))
    approved_oil = int(request.form.get("approved_oil", 0))

    demand.approved_sugar = approved_sugar
    demand.approved_oil = approved_oil
    demand.status = "Approved"
    db.session.commit()

    flash(f"Demand {demand_id} approved! (Sugar: {approved_sugar}kg, Oil: {approved_oil}kg)", "success")
    return redirect(url_for("admin_demands"))

@app.route("/mark_delivered/<int:demand_id>", methods=["POST"])
def mark_delivered(demand_id):
    demand = Demand.query.get_or_404(demand_id)
    demand.status = "Delivered"
    db.session.commit()
    flash(f"Demand {demand_id} marked as Delivered!", "success")
    return redirect(url_for("delivery_page"))


@app.route("/admin")
def admin_master():
    if not session.get("admin_logged_in"):
        return redirect(url_for("admin_login"))
    return render_template("admin_master.html")

@app.route("/admin/demands")
def admin_demands():
    demands = Demand.query.all()
    return render_template("admin.html", demands=demands)


@app.route("/delivery")
def delivery_page():
    if not session.get("delivery_logged_in"):
        return redirect(url_for("delivery_login"))
    demands = Demand.query.filter_by(status="Approved").all()        
    return render_template("delivery.html", demands=demands)
@app.route("/admin/employees")
def admin_employees():
    employees = Employee.query.all()
    return render_template("admin_employees.html", employees=employees)

@app.route("/admin/approve/<int:emp_id>", methods=["POST"])
def approve_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    emp.status = "Active"
    db.session.commit()
    return redirect(url_for("admin_employees"))

@app.route("/admin/reject/<int:emp_id>", methods=["POST"])
def reject_employee(emp_id):
    emp = Employee.query.get_or_404(emp_id)
    emp.status = "Rejected"
    db.session.commit()
    return redirect(url_for("admin_employees"))

@app.route("/admin_login", methods=["GET", "POST"])
def admin_login():
    error = None
    if request.method == "POST":
        if request.form["username"] == "admin" and request.form["password"] == "admin123":
            session["admin_logged_in"] = True
            return redirect(url_for("admin_master"))
        else:
            error = "Invalid Credentials"
    return render_template("login.html", role="Admin", error=error)


@app.route("/delivery_login", methods=["GET", "POST"])
def delivery_login():
    error = None
    if request.method == "POST":
        if request.form["username"] == "delivery" and request.form["password"] == "delivery123":
            session["delivery_logged_in"] = True
            return redirect(url_for("delivery_page"))
        else:
            error = "Invalid Credentials"
    return render_template("login.html", role="Delivery", error=error)


@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))

