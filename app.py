from flask import Flask, render_template, session, redirect, request
from flask_session import Session
from tempfile import mkdtemp
from werkzeug.security import check_password_hash, generate_password_hash
import sqlite3



app = Flask("__name__")

# Ensure templates are auto-reloaded
app.config["TEMPLATES_AUTO_RELOAD"] = True

# Configure session to use filesystem (instead of signed cookies)
app.config["SESSION_FILE_DIR"] = mkdtemp()
app.config["SESSION_PERMANENT"] = False
app.config["SESSION_TYPE"] = "filesystem"
Session(app)

# Connect with the db
db = sqlite3.connect("project.db")
cursor = db.cursor()


@app.route("/")
def index():
    """ TODO """
    return render_template("index.html")


@app.route("/login", methods=["GET","POST"])
def login():
    """ TODO """
    if request.method == "POST":
        return redirect("/")
    return render_template("login.html")


@app.route("/register", methods=["GET", "POST"])
def register():
    
    if request.method == "POST":
        username = request.form.get("username")
        email = request.form.get("email")
        password = request.form.get("password")

        password = generate_password_hash(password)
        
        cursor.executemany("INSERT INTO users (username, email, hash) VALUES (?, ?, ?)", 
                        username, email, password)
        db.commit()

        return redirect("/register")

    return render_template("register.html")


@app.route("/log_out")
def log_out():
    """ TODO """
    return ("log out")


@app.route("/new_activity", methods=["GET", "POST"])
def new_activity():
    """ TODO """
    return "new activity"
