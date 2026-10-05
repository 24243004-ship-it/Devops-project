from flask import (
    Flask, request, redirect, url_for,
    session, flash, render_template_string
)
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
import os

# =========================================================
# APP CONFIGURATION
# =========================================================

app = Flask(__name__)

app.secret_key = "smart_resume_tracker_secret"

app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///job_tracker.db"
app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

db = SQLAlchemy(app)

# Resume upload folder
UPLOAD_FOLDER = "resumes"

if not os.path.exists(UPLOAD_FOLDER):
    os.makedirs(UPLOAD_FOLDER)

app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER


# =========================================================
# DATABASE MODEL
# =========================================================

class JobApplication(db.Model):

    id = db.Column(db.Integer, primary_key=True)

    company = db.Column(db.String(100), nullable=False)

    role = db.Column(db.String(100), nullable=False)

    location = db.Column(db.String(100), nullable=False)

    application_date = db.Column(
        db.String(50),
        nullable=False
    )

    status = db.Column(
        db.String(50),
        default="Applied"
    )

    salary = db.Column(
        db.String(50),
        default="Not Specified"
    )

    notes = db.Column(
        db.Text,
        default=""
    )


# =========================================================
# HTML + CSS
# =========================================================

BASE_STYLE = """

<style>

* {
    box-sizing: border-box;
}

body {
    margin: 0;
    font-family: Arial, sans-serif;
    background: #f4f7fb;
    color: #333;
}

/* NAVBAR */

.navbar {
    background: #173b8f;
    color: white;
    padding: 18px 6%;
    display: flex;
    justify-content: space-between;
    align-items: center;
}

.navbar h2 {
    margin: 0;
}

.navbar a {
    color: white;
    text-decoration: none;
    font-weight: bold;
}


/* MAIN */

.container {
    width: 92%;
    margin: 30px auto;
}


/* HERO */

.hero {
    background: white;
    padding: 30px;
    border-radius: 15px;
    margin-bottom: 25px;
    box-shadow: 0 4px 15px rgba(0,0,0,0.08);
}

.hero h1 {
    color: #173b8f;
    margin-bottom: 8px;
}


/* STATS */

.stats {
    display: grid;
    grid-template-columns: repeat(4, 1fr);
    gap: 20px;
    margin-bottom: 25px;
}

.stat {
    background: white;
    padding: 20px;
    border-radius: 12px;
    text-align: center;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.stat h3 {
    margin: 0;
    color: #555;
}

.stat p {
    font-size: 30px;
    font-weight: bold;
    color: #173b8f;
}


/* CARDS */

.card {
    background: white;
    padding: 25px;
    border-radius: 12px;
    margin-bottom: 25px;
    box-shadow: 0 3px 12px rgba(0,0,0,0.08);
}

.card h2 {
    color: #173b8f;
}


/* FORM */

input,
select,
textarea {
    width: 100%;
    padding: 12px;
    margin: 7px 0 15px;
    border: 1px solid #ccc;
    border-radius: 7px;
    font-size: 14px;
}

textarea {
    height: 100px;
}

button {
    background: #173b8f;
    color: white;
    border: none;
    padding: 11px 18px;
    border-radius: 7px;
    cursor: pointer;
    font-weight: bold;
}

button:hover {
    background: #0d2868;
}


/* TABLE */

table {
    width: 100%;
    border-collapse: collapse;
}

th {
    background: #173b8f;
    color: white;
    padding: 12px;
}

td {
    padding: 12px;
    border-bottom: 1px solid #ddd;
    text-align: center;
}


/* STATUS */

.status {
    padding: 6px 10px;
    border-radius: 15px;
    background: #e3f2fd;
    color: #1565c0;
    font-weight: bold;
}


/* MESSAGE */

.message {
    padding: 12px;
    background: #e8f5e9;
    color: #2e7d32;
    border-radius: 7px;
    margin-bottom: 15px;
}


/* LOGIN */

.login-box {
    width: 400px;
    margin: 80px auto;
    background: white;
    padding: 35px;
    border-radius: 15px;
    box-shadow: 0 5px 25px rgba(0,0,0,0.1);
}

.login-box h1 {
    text-align: center;
    color: #173b8f;
}

.login-box button {
    width: 100%;
}


/* FILTER */

.filter {
    display: grid;
    grid-template-columns: 2fr 1fr 1fr auto;
    gap: 10px;
    align-items: center;
}


/* RESPONSIVE */

@media(max-width: 900px) {

    .stats {
        grid-template-columns: 1fr 1fr;
    }

    .filter {
        grid-template-columns: 1fr;
    }

    table {
        font-size: 12px;
    }
}

</style>
"""


# =========================================================
# LOGIN PAGE
# =========================================================

LOGIN_PAGE = """

<!DOCTYPE html>

<html>

<head>

<title>Smart Resume Tracker</title>

""" + BASE_STYLE + """

</head>

<body>

<div class="login-box">

<h1>Smart Resume & Job Tracker</h1>

<p style="text-align:center;">
Track your job applications in one place.
</p>

{% with messages = get_flashed_messages() %}

{% for message in messages %}

<div class="message">
{{ message }}
</div>

{% endfor %}

{% endwith %}


<form method="POST">

<label>Username</label>

<input
type="text"
name="username"
placeholder="Enter username"
required
>


<label>Password</label>

<input
type="password"
name="password"
placeholder="Enter password"
required
>


<button type="submit">
Login
</button>

</form>


<p style="text-align:center;margin-top:20px;">

New user?

<a href="/register">
Create Account
</a>

</p>

</div>

</body>

</html>

"""


# =========================================================
# REGISTER PAGE
# =========================================================

REGISTER_PAGE = """

<!DOCTYPE html>

<html>

<head>

<title>Register</title>

""" + BASE_STYLE + """

</head>

<body>

<div class="login-box">

<h1>Create Account</h1>


{% with messages = get_flashed_messages() %}

{% for message in messages %}

<div class="message">
{{ message }}
</div>

{% endfor %}

{% endwith %}


<form method="POST">

<label>Username</label>

<input
type="text"
name="username"
placeholder="Create username"
required
>


<label>Password</label>

<input
type="password"
name="password"
placeholder="Create password"
required
>


<button type="submit">
Register
</button>

</form>


<p style="text-align:center;">

Already registered?

<a href="/login">
Login
</a>

</p>

</div>

</body>

</html>

"""


# =========================================================
# DASHBOARD
# =========================================================

DASHBOARD_PAGE = """

<!DOCTYPE html>

<html>

<head>

<title>Job Tracker Dashboard</title>

""" + BASE_STYLE + """

</head>

<body>


<div class="navbar">

<h2>Smart Job Tracker</h2>

<div>

Welcome, {{ username }}

&nbsp; | &nbsp;

<a href="/logout">
Logout
</a>

</div>

</div>


<div class="container">


<div class="hero">

<h1>
Smart Resume & Job Application Tracker
</h1>

<p>
Manage your companies, job roles, application status
and interview progress from one dashboard.
</p>

</div>


{% with messages = get_flashed_messages() %}

{% for message in messages %}

<div class="message">
{{ message }}
</div>

{% endfor %}

{% endwith %}


<!-- STATISTICS -->

<div class="stats">


<div class="stat">

<h3>Total Applications</h3>

<p>
{{ total }}
</p>

</div>


<div class="stat">

<h3>Applied</h3>

<p>
{{ applied }}
</p>

</div>


<div class="stat">

<h3>Interviews</h3>

<p>
{{ interview }}
</p>

</div>


<div class="stat">

<h3>Selected</h3>

<p>
{{ selected }}
</p>

</div>


</div>


<!-- RESUME -->

<div class="card">

<h2>Resume Manager</h2>

<form
action="/upload_resume"
method="POST"
enctype="multipart/form-data"
>

<input
type="file"
name="resume"
accept=".pdf,.doc,.docx"
required
>

<button type="submit">
Upload Resume
</button>

</form>

</div>


<!-- ADD APPLICATION -->

<div class="card">

<h2>Add Job Application</h2>

<form action="/add_application" method="POST">


<label>Company Name</label>

<input
type="text"
name="company"
placeholder="Example: Accenture"
required
>


<label>Job Role</label>

<input
type="text"
name="role"
placeholder="Example: Data Analyst"
required
>


<label>Location</label>

<input
type="text"
name="location"
placeholder="Example: Chennai"
required
>


<label>Application Date</label>

<input
type="date"
name="application_date"
required
>


<label>Salary</label>

<input
type="text"
name="salary"
placeholder="Example: 6 LPA"
>


<label>Status</label>

<select name="status">

<option value="Applied">
Applied
</option>

<option value="Interview">
Interview
</option>

<option value="Selected">
Selected
</option>

<option value="Rejected">
Rejected
</option>

</select>


<label>Notes</label>

<textarea
name="notes"
placeholder="Add interview or company notes..."
></textarea>


<button type="submit">
Add Application
</button>

</form>

</div>


<!-- FILTER -->

<div class="card">

<h2>Search Applications</h2>

<form method="GET" action="/dashboard">

<div class="filter">

<input
type="text"
name="search"
placeholder="Search company or role"
value="{{ search }}"
>


<select name="status_filter">

<option value="">
All Status
</option>

<option value="Applied">
Applied
</option>

<option value="Interview">
Interview
</option>

<option value="Selected">
Selected
</option>

<option value="Rejected">
Rejected
</option>

</select>


<button type="submit">
Search
</button>

<a href="/dashboard">
<button type="button">
Reset
</button>
</a>

</div>

</form>

</div>


<!-- APPLICATION TABLE -->

<div class="card">

<h2>My Job Applications</h2>


{% if applications %}

<table>

<tr>

<th>ID</th>
<th>Company</th>
<th>Role</th>
<th>Location</th>
<th>Date</th>
<th>Status</th>
<th>Salary</th>
<th>Action</th>

</tr>


{% for job in applications %}

<tr>

<td>
JOB{{ job.id }}
</td>

<td>
{{ job.company }}
</td>

<td>
{{ job.role }}
</td>

<td>
{{ job.location }}
</td>

<td>
{{ job.application_date }}
</td>

<td>

<span class="status">

{{ job.status }}

</span>

</td>

<td>
{{ job.salary }}
</td>

<td>

<a
href="/delete/{{ job.id }}"
onclick="return confirm('Delete this application?')"
>

Delete

</a>

</td>

</tr>

{% endfor %}

</table>


{% else %}

<p>
No job applications found.
</p>

{% endif %}

</div>


</div>

</body>

</html>

"""


# =========================================================
# HOME
# =========================================================

@app.route("/")
def home():

    if "username" in session:
        return redirect("/dashboard")

    return redirect("/login")


# =========================================================
# LOGIN
# =========================================================

@app.route("/login", methods=["GET", "POST"])
def login():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # Simple demo authentication
        # Default account:
        # username: admin
        # password: admin123

        if username == "admin" and password == "admin123":

            session["username"] = username

            return redirect("/dashboard")

        flash("Invalid username or password.")

    return render_template_string(LOGIN_PAGE)


# =========================================================
# REGISTER
# =========================================================

@app.route("/register", methods=["GET", "POST"])
def register():

    if request.method == "POST":

        username = request.form["username"]

        password = request.form["password"]

        # For this simple version, registration
        # is stored in session-based demo.

        session["username"] = username

        flash("Account created successfully!")

        return redirect("/dashboard")

    return render_template_string(REGISTER_PAGE)


# =========================================================
# DASHBOARD
# =========================================================

@app.route("/dashboard")
def dashboard():

    if "username" not in session:

        return redirect("/login")


    search = request.args.get(
        "search",
        ""
    )

    status_filter = request.args.get(
        "status_filter",
        ""
    )


    # Build query

    query = JobApplication.query


    if search:

        query = query.filter(
            db.or_(
                JobApplication.company.ilike(
                    f"%{search}%"
                ),

                JobApplication.role.ilike(
                    f"%{search}%"
                )
            )
        )


    if status_filter:

        query = query.filter_by(
            status=status_filter
        )


    applications = query.order_by(
        JobApplication.id.desc()
    ).all()


    # Statistics

    total = JobApplication.query.count()

    applied = JobApplication.query.filter_by(
        status="Applied"
    ).count()

    interview = JobApplication.query.filter_by(
        status="Interview"
    ).count()

    selected = JobApplication.query.filter_by(
        status="Selected"
    ).count()


    return render_template_string(

        DASHBOARD_PAGE,

        username=session["username"],

        applications=applications,

        total=total,

        applied=applied,

        interview=interview,

        selected=selected,

        search=search

    )


# =========================================================
# ADD APPLICATION
# =========================================================

@app.route(
    "/add_application",
    methods=["POST"]
)
def add_application():

    if "username" not in session:

        return redirect("/login")


    company = request.form["company"]

    role = request.form["role"]

    location = request.form["location"]

    application_date = request.form[
        "application_date"
    ]

    status = request.form["status"]

    salary = request.form.get(
        "salary",
        "Not Specified"
    )

    notes = request.form.get(
        "notes",
        ""
    )


    job = JobApplication(

        company=company,

        role=role,

        location=location,

        application_date=application_date,

        status=status,

        salary=salary,

        notes=notes

    )


    db.session.add(job)

    db.session.commit()


    flash(
        "Job application added successfully!"
    )


    return redirect("/dashboard")


# =========================================================
# DELETE APPLICATION
# =========================================================

@app.route("/delete/<int:job_id>")
def delete_application(job_id):

    if "username" not in session:

        return redirect("/login")


    job = JobApplication.query.get_or_404(
        job_id
    )


    db.session.delete(job)

    db.session.commit()


    flash(
        "Job application deleted."
    )


    return redirect("/dashboard")


# =========================================================
# RESUME UPLOAD
# =========================================================

@app.route(
    "/upload_resume",
    methods=["POST"]
)
def upload_resume():

    if "username" not in session:

        return redirect("/login")


    file = request.files.get(
        "resume"
    )


    if not file:

        flash("Please select a resume.")

        return redirect("/dashboard")


    filename = file.filename


    allowed = (
        ".pdf",
        ".doc",
        ".docx"
    )


    if not filename.lower().endswith(
        allowed
    ):

        flash(
            "Only PDF, DOC and DOCX files are allowed."
        )

        return redirect("/dashboard")


    file.save(
        os.path.join(
            app.config["UPLOAD_FOLDER"],
            filename
        )
    )


    flash(
        "Resume uploaded successfully!"
    )


    return redirect("/dashboard")


# =========================================================
# LOGOUT
# =========================================================

@app.route("/logout")
def logout():

    session.clear()

    return redirect("/login")


# =========================================================
# CREATE DATABASE
# =========================================================

with app.app_context():

    db.create_all()


# =========================================================
# RUN
# =========================================================

if __name__ == "__main__":

    print("=" * 55)

    print(
        "SMART RESUME & JOB APPLICATION TRACKER"
    )

    print("=" * 55)

    print(
        "Demo Username : admin"
    )

    print(
        "Demo Password : admin123"
    )

    print(
        "URL            : http://127.0.0.1:5000"
    )

    print("=" * 55)

    app.run(
        debug=True
    )