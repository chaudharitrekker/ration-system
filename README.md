🛒 e-Ration Demand System

A web-based ration demand and approval system built with Python Flask and PostgreSQL.
The system allows users to request ration items, approvers to validate requests, and suppliers to deliver approved items.
🚀 Features

    👤 User Login & Registration – Employees can register with a Ration ID and login securely.

    📝 Demand Requests – Users can place ration requests (e.g., 5kg Sugar).

    ✅ Admin Approval – Admin can approve, partially approve, or reject demands.

    🚚 Supplier Delivery – Suppliers deliver items to the provided address.

    🔒 Role-Based Access – Separate dashboards for Admin, Employees, and Suppliers.

    💾 Database Persistence – PostgreSQL used for storing users, ration items, and demand status.

    🎨 Responsive UI – Clean HTML, CSS (custom theme with 🇮🇳 colors).

⚙️ Installation & Setup
1️⃣ Clone the repository

git clone git@github.com:chaudharitrekker/ration-system.git
cd ration-system

2️⃣ Create virtual environment

python3 -m venv venv
source venv/bin/activate   # On Linux/Mac
venv\Scripts\activate      # On Windows

3️⃣ Install dependencies

pip install -r requirements.txt

4️⃣ Setup database (PostgreSQL)

# Example
createdb ration_system
export DATABASE_URL=postgresql://username:password@localhost/ration_system

Run migrations:

flask db upgrade

5️⃣ Start the server

flask run

App will run at:
👉 http://127.0.0.1:5000/
🧑‍💻 Roles

    Employee (User) – Register, Login, Place ration demand.

    Admin – Approve / Reject employee registrations & ration demands.

    Supplier – View approved demands and mark as delivered.

🛠️ Tech Stack

    Backend: Python Flask

    Database: PostgreSQL + SQLAlchemy

    Frontend: HTML, CSS (Custom, Responsive Design)

    Version Control: Git + GitHub

    Deployment: AWS (future-ready)

🤝 Contribution

    Fork the repo

    Create feature branch

    Commit changes

    Push to branch

    Create Pull Request

📜 License

This project is licensed under the MIT License.
