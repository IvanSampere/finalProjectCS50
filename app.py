import os

from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
from cs50 import SQL



app = Flask("__name__")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect with the db
db = SQL('sqlite:///project.db')

@app.route("/")
def index():
    """ TODO """
    return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def login():
    # Forget any user id
    session.clear()

    if request.method == "POST":
        # Get the data from the form
        username = request.form.get("username")
        password = request.form.get("password")
        # Query database for username
        row_user = db.execute("SELECT * FROM users WHERE username = ?", username)
        # Check the username exist and the password is correct
        if len(row_user) == 1 and check_password_hash(row_user[0]['hash'], password):
            session['user_id'] = row_user[0]['id']
        # redirect to the index
        return redirect("/")
    
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        # Get the data from the form
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")
        # Generate a password hash
        password = generate_password_hash(password)
        # Execute a query to insert the data to the table users
        db.execute("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", 
                    username, email, password)
        # Login directly
        login()
        # redirect to the index
        return redirect("/")
    return render_template("register.html")


@app.route("/log_out")
def log_out():
    # forget any user_id
    session.clear()
    # redirect to the index
    return redirect("/")


@app.route("/new_activity", methods=["GET", "POST"])
def new_activity():
    """ TODO """
    return "new activity"
