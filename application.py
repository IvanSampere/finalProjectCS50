from flask import Flask, render_template, session, redirect, request


app = Flask("__name__")

@app.route("/")
def index():
    return render_template("index.html")

@app.route("/login", methods=["GET","POST"])
def login():
    if request.method == "POST":
        return redirect("/")
    return render_template("login.html")


if __name__ == "__main__":
    app.run()

