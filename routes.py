from flask import render_template, request, redirect, url_for, flash, session, send_file
from werkzeug.utils import secure_filename
from app import app, db
from models import Demand, User, OfficerDemand
from forms import LoginForm, DemandForm, OfficerDemandForm
from ldap3 import Server, Connection, ALL, ALL_ATTRIBUTES
from forms import LoginForm
from reportlab.lib.pagesizes import A4
from reportlab.pdfgen import canvas
import io
import os
from datetime import datetime
import re


UPLOAD_FOLDER = os.path.join("static", "uploads")
os.makedirs(UPLOAD_FOLDER, exist_ok=True)
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


LDAP_SERVER = "ldap://localhost:389"
LDAP_USER_DN = "cn=admin,dc=navy,dc=local"
LDAP_PASSWORD = "admin123"
BASE_DN = "dc=navy,dc=local"

app.config["LDAP_SERVER"] = "ldap://localhost:389"
app.config["LDAP_USER_DN"] = "cn=admin,dc=navy,dc=local"
app.config["LDAP_PASSWORD"] = "admin123"
app.config["BASE_DN"] = "dc=navy,dc=local"
app.secret_key = "super_secret_key"


@app.route("/")
def index():
    return redirect(url_for("login"))
    
def ldap_authenticate(employee_number, password):
    """Authenticate officer via LDAP using employeeNumber"""
    try:
        server = Server(app.config["LDAP_SERVER"], get_info=ALL)
        conn = Connection(
            server,
            user=app.config["LDAP_USER_DN"],
            password=app.config["LDAP_PASSWORD"],
            auto_bind=True,
        )

        # Search officer by employeeNumber
        search_filter = f"(employeeNumber={employee_number})"
        conn.search(app.config["BASE_DN"], search_filter, attributes=ALL_ATTRIBUTES)

        if not conn.entries:
            return False

        user_entry = conn.entries[0]
        user_dn = user_entry.entry_dn

        # Rebind as the officer with given password
        user_conn = Connection(server, user=user_dn, password=password)
        if not user_conn.bind():
            return False

        # ✅ Extract officer attributes safely
        officer_data = {
            "employeeNumber": str(user_entry.employeeNumber) if hasattr(user_entry, "employeeNumber") else None,
            "name": str(user_entry.cn) if hasattr(user_entry, "cn") else None,
            "rank": str(user_entry.title) if hasattr(user_entry, "title") else None,
            "description": str(user_entry.description) if hasattr(user_entry, "description") else "",
        }
        return officer_data
    except Exception as e:
        print("LDAP Auth failed:", e)
        return False


@app.route("/login", methods=["GET", "POST"])
def login():
    form = LoginForm()
    if form.validate_on_submit():
        username = form.username.data.strip()
        password = form.password.data.strip()

        # 1️⃣ Check DB for raiser/issuer first
        user = User.query.filter_by(username=username).first()
        if user and user.check_password(password):
            session["user_id"] = user.id
            session["role"] = user.role
            flash(f"✅ Logged in as {session['role']}", "success")

            if user.role == "raiser":
                return redirect(url_for("raiser_dashboard"))
            elif user.role == "issuer":
                return redirect(url_for("issuer_dashboard"))

        # 2️⃣ Check LDAP for officer login
        ldap_entry = ldap_authenticate(username, password)
        if ldap_entry:
            session["employee_number"] = ldap_entry.get("employeeNumber")
            session["name"] = ldap_entry.get("name", "Unknown Officer")
            session["rank"] = ldap_entry.get("rank", "Unknown Rank")
            session["role"] = "officer"

            # ✅ Optional: parse rank from description if available
            desc = ldap_entry.get("description", "")
            if desc and not session["rank"]:
                rank_match = re.search(r"Rank=(\w+)", desc)
                if rank_match:
                    session["rank"] = rank_match.group(1)

            flash("✅ Logged in as Officer", "success")
            return redirect(url_for("officer_dashboard"))

        # ❌ Invalid credentials
        flash("❌ Invalid username or password", "danger")

    return render_template("home.html", form=form)

@app.route("/officer")
def officer_dashboard():
    if session.get("role") != "officer":
        return redirect(url_for("login"))
    return render_template("officer_dashboard.html")

	

@app.route("/officer/new", methods=["GET", "POST"])
def officer_new_demand():
    if session.get("role") != "officer":
        return redirect(url_for("login"))

    form = OfficerDemandForm()

    
    if not form.unit.choices:
        with open("units.txt") as f:
            units = [(line.strip(), line.strip()) for line in f.readlines()]
        form.unit.choices = units

    if form.validate_on_submit():
        # Handle file upload
        filename = None
        file = form.rik_gx_file.data
        if file:
            filename = secure_filename(file.filename)
            upload_folder = app.config.get("UPLOAD_FOLDER", "uploads")
            os.makedirs(upload_folder, exist_ok=True)
            file.save(os.path.join(upload_folder, filename))

        demand = OfficerDemand(
            employee_number=session.get("employee_number"),   # ✅ Fix
            name=session.get("name", "Unknown Officer"),
            rank=session.get("rank", "Unknown Rank"),
            ration_type=form.ration_type.data,
            address=form.address.data,
            unit=form.unit.data,
            office_phone=form.office_phone.data,
            mobile=form.mobile.data,
            collection_type=form.collection_type.data,
            bank_account=form.bank_account.data,
            ifsc=form.ifsc.data,
            rik_gx_number=form.rik_gx_number.data,
            rik_gx_date=form.rik_gx_date.data,
            rik_gx_file=filename,
            retirement_date=form.retirement_date.data,
            promotion_gx_number=form.promotion_gx_number.data,
            promotion_gx_date=form.promotion_gx_date.data,
            created_by=session.get("employee_number")
        )
        db.session.add(demand)
        db.session.commit()
        flash("✅ Demand submitted successfully!", "success")
        return redirect(url_for("officer_previous_demands"))

    elif request.method == "POST":
        flash("❌ Please check the form errors.", "danger")

    return render_template("officer_form.html", form=form)

@app.route("/officer/previous")
def officer_previous_demands():
    if session.get("role") != "officer":
        return redirect(url_for("login"))
    demands = OfficerDemand.query.filter_by(employee_number=session["employee_number"]).all()
    return render_template("officer_previous.html", demands=demands)    

@app.route("/officer/view/<int:demand_id>")
def officer_view_demand(demand_id):
    if session.get("role") != "officer":
        return redirect(url_for("login"))

    demand = OfficerDemand.query.get_or_404(demand_id)
    return render_template("officer_view.html", demand=demand)

@app.route("/officer/pdf/<int:demand_id>")
def officer_pdf(demand_id):
    demand = OfficerDemand.query.get_or_404(demand_id)

    # Create PDF in memory
    buffer = io.BytesIO()
    p = canvas.Canvas(buffer, pagesize=A4)
    width, height = A4

    y = height - 50
    p.setFont("Helvetica-Bold", 14)
    p.drawString(200, y, "RIK COMMENCEMENT FORM")
    y -= 40

    p.setFont("Helvetica", 12)
    fields = [
        ("Name", demand.name),
        ("Rank", demand.rank),
        ("P. No.", demand.employee_number),
        ("Ration Type", demand.ration_type),
        ("Address", demand.address),
        ("Unit", demand.unit),
        ("Office Phone", demand.office_phone),
        ("Mobile", demand.mobile),
        ("Collection Type", demand.collection_type),
        ("Bank Account", demand.bank_account),
        ("IFSC", demand.ifsc),
        ("RIK GX Number", demand.rik_gx_number),
        ("RIK GX Date", str(demand.rik_gx_date)),
        ("Retirement Date", str(demand.retirement_date) if demand.retirement_date else ""),
        ("Promotion GX Number", demand.promotion_gx_number or ""),
        ("Promotion GX Date", str(demand.promotion_gx_date) if demand.promotion_gx_date else "")
    ]

    for label, value in fields:
        p.drawString(50, y, f"{label}: {value}")
        y -= 20

    p.showPage()
    p.save()
    buffer.seek(0)

    return send_file(buffer, as_attachment=True, download_name=f"demand_{demand.id}.pdf", mimetype="application/pdf")


@app.route("/raiser")
def raiser_dashboard():
    if session.get("role") != "raiser":
        return redirect(url_for("login"))
    return render_template("raiser_dashboard.html")

@app.route("/raiser/add", methods=["GET", "POST"])
def raiser_add_officer():
    if session.get("role") != "raiser":
        flash("❌ Unauthorized", "danger")
        return redirect(url_for("login"))

    form = OfficerDemandForm()
    
    if not form.unit.choices:
        with open("units.txt") as f:
            units = [(line.strip(), line.strip()) for line in f.readlines()]
        form.unit.choices = units

    if form.validate_on_submit():
        filename = None
        if form.rik_gx_file.data:
            file = form.rik_gx_file.data
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config["UPLOAD_FOLDER"], filename))

        demand = OfficerDemand(
            employee_number=form.employee_number.data,
            name=form.name.data,
            rank=form.rank.data,
            ration_type=form.ration_type.data,
            address=form.address.data,
            unit=form.unit.data,
            office_phone=form.office_phone.data,
            mobile=form.mobile.data,
            collection_type=form.collection_type.data,
            bank_account=form.bank_account.data,
            ifsc=form.ifsc.data,
            rik_gx_number=form.rik_gx_number.data,
            rik_gx_date=form.rik_gx_date.data,
            rik_gx_file=filename,
            retirement_date=form.retirement_date.data,
            promotion_gx_number=form.promotion_gx_number.data,
            promotion_gx_date=form.promotion_gx_date.data,
            created_by="raiser"
        )
        db.session.add(demand)
        db.session.commit()
        flash("✅ Officer Ration Request added successfully", "success")
        return redirect(url_for("raiser_dashboard"))

    return render_template("raiser_add_officer.html", form=form)

    
@app.route("/raiser/approve", methods=["GET", "POST"])
def raiser_approve_demands():
    if session.get("role") != "raiser":
        return redirect(url_for("login"))

    # ✅ Handle Approve action
    if request.method == "POST":
        demand_id = request.form.get("demand_id")
        demand = OfficerDemand.query.get(demand_id)
        if demand:
            demand.status = "Approved"
            db.session.commit()
            flash("✅ Request approved successfully", "success")
        else:
            flash("❌ Demand not found", "danger")
        return redirect(url_for("raiser_approve_demands"))

    # ✅ Search + Pagination
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10

    query = OfficerDemand.query.filter_by(status="Pending")

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            (OfficerDemand.employee_number.ilike(like_pattern)) |
            (OfficerDemand.name.ilike(like_pattern)) |
            (OfficerDemand.rank.ilike(like_pattern)) |
            (OfficerDemand.unit.ilike(like_pattern))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    demands = pagination.items

    return render_template("raiser_approve.html", demands=demands, pagination=pagination, search=search)


@app.route("/raiser/master", methods=["GET", "POST"])
def raiser_master_list():
    if session.get("role") != "raiser":
        return redirect(url_for("login"))

    # 🔎 Search + Pagination
    search = request.args.get("search", "").strip()
    page = request.args.get("page", 1, type=int)
    per_page = 10

    query = OfficerDemand.query.filter_by(status="Approved")

    if search:
        like_pattern = f"%{search}%"
        query = query.filter(
            (OfficerDemand.employee_number.ilike(like_pattern)) |
            (OfficerDemand.name.ilike(like_pattern)) |
            (OfficerDemand.rank.ilike(like_pattern)) |
            (OfficerDemand.unit.ilike(like_pattern))
        )

    pagination = query.paginate(page=page, per_page=per_page, error_out=False)
    demands = pagination.items

    return render_template("raiser_master.html", demands=demands, pagination=pagination, search=search)

@app.route("/raiser/delete/<int:demand_id>", methods=["POST"])
def raiser_delete_demand(demand_id):
    if session.get("role") != "raiser":
        return redirect(url_for("login"))

    demand = OfficerDemand.query.get_or_404(demand_id)
    db.session.delete(demand)
    db.session.commit()
    flash("🗑️ Ration Request deleted", "info")
    return redirect(url_for("raiser_master_list"))

@app.route("/issuer")
def issuer_dashboard():
    return "Issuer Dashboard (Issue Approved Demands + Manage Stock)"   

@app.route("/logout")
def logout():
    session.clear()
    return redirect(url_for("home"))




