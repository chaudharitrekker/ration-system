from flask import render_template, request, redirect, url_for, flash, session
from app import app, db
from models import Demand
from forms import LoginForm, DemandForm
from ldap3 import Server, Connection, ALL



LDAP_SERVER = "ldap://localhost:389"
LDAP_USER_DN = "cn=admin,dc=navy,dc=local"
LDAP_PASSWORD = "admin123"
BASE_DN = "dc=navy,dc=local"

app.secret_key = "super_secret_key"

@app.route("/")
def home():
    return render_template("home.html")

@app.route("/login", methods=["GET", "POST"])
def user_login():
    form = LoginForm()
    error = None
    if form.validate_on_submit():
        employee_code = form.employee_code.data
        password = form.password.data

        try:
            # Step 1: Connect as admin to search DN
            server = Server(LDAP_SERVER, get_info=ALL)
            conn = Connection(server, user=LDAP_USER_DN, password=LDAP_PASSWORD, auto_bind=True)

            # Step 2: Search user by employeeNumber
            conn.search(BASE_DN, f"(employeeNumber={employee_code})", attributes=["uid"])
            if not conn.entries:
                error = "❌ Employee not found."
            else:
                user_dn = conn.entries[0].entry_dn

                # Step 3: Try binding with user DN + entered password
                user_conn = Connection(server, user=user_dn, password=password)
                if user_conn.bind():
                    session["employee_code"] = employee_code
                    flash("✅ Login successful!", "success")
                    return redirect(url_for("demand"))
                else:
                    error = "❌ Invalid credentials."
        except Exception as e:
            error = f"LDAP error: {str(e)}"

    return render_template("login.html", role="User", form=form, error=error)
   
@app.route("/demand", methods=["GET", "POST"])
def demand():
    if not session.get("employee_code"):
        flash("⚠️ Please login first!", "warning")
        return redirect(url_for("user_login"))

    form = DemandForm()
    if form.validate_on_submit():
        new_demand = Demand(
            requested_sugar=form.sugar_kg.data,
            requested_oil=form.oil_kg.data,
            employee_code=session["employee_code"]  # ✅ ab sahi column use ho raha hai
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

