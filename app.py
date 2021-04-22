import os

from flask import Flask, render_template, session, redirect, request, flash
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
        username = request.form.get("username") # Also for the email
        password = request.form.get("password")
        # Query database for username
        row_user = db.execute("SELECT * FROM users WHERE username = ? OR email = ?", username, username)
        # Check the username exist and the password is correct
        if len(row_user) != 1 or not check_password_hash(row_user[0]['hash'], password):
            flash("Invalid user/email or password")
            return render_template("login.html")

        # Keep the data from the session
        session['user_id'] = row_user[0]['id']
        session['username'] = row_user[0]['username']
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
        # Ensure the username is not taken
        usernames = db.execute("SELECT * FROM users")
        for username_list in usernames:
            if username == username_list['username']:
                flash("The username already taken")
                return redirect("/register")
            if email == username_list['email']:
                flash("The email already exist, try to log in")
                return redirect("/register")
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


@app.route("/content", methods=['GET', 'POST'])
def content():
    """ TODO """
    if request.method == 'POST':
        tag = request.form.getlist("tag")
        print(tag[0])
        return redirect("/content")
    else:
        content = request.args.get("q")
        return render_template("content.html")


@app.route("/activity", methods=["GET", "POST"])
def activity():
    """ TODO """
    return render_template("activity.html")


@app.route("/my_activities")
def my_activities():
    # Get the activity info 
    activities = db.execute("SELECT * FROM activities WHERE user_id = ?", 
                            session['user_id'])
    # Get the explanation and put in every row a tag <br> for the html
    explanation = ""
    for aux in range(len(activities)):
        for letter in activities[aux]['explanation']:
            explanation += letter
            if letter == "\r":
                explanation+="<br>"

        activities[aux]['explanation'] = explanation
        explanation = ""

    return render_template("my_activities.html", activities=activities)


@app.route("/new_activity", methods=['GET', 'POST'])
def new_activity():
    if request.method == 'POST': 
        # Get the data from the html form
        title = request.form.get('title')
        tags = request.form.getlist('tag')
        ages = request.form.getlist('age')
        explanation = request.form.get('explanation')
        activity = request.form.get('activity')
        # Inser into the activities table the title, the text areas and the user id
        activity_id = db.execute('INSERT INTO activities(title, explanation, activity, user_id) VALUES (?,?,?,?)',
                                    title, explanation, activity, session['user_id'])
        # Get the name of the tags and inserts into their table
        for tag in tags:
            db.execute('INSERT INTO tags(name, activity_id) VALUES (?,?)',
                        tag, activity_id)
        # Get the name of the ages and inserts into their table
        for age in ages:
            db.execute('INSERT INTO ages(age, activity_id) VALUES (?,?)',
                        age, activity_id)
        flash("New Activity write succesfully!")
        return redirect("/new_activity")
    
    return render_template("new_activity.html")


@app.route("/delete")
def delete_activity():
    """ TODO """
    return "TODO"

