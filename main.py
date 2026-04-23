from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
import os
import db

load_dotenv()

app = Flask(__name__)
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def Home():
    if not session.get('username'):
        return redirect("/login")
    sessionsData = db.GetAllSessions(session['id'])
    return render_template("index.html", sessions=sessionsData)

@app.route("/login", methods=["GET", "POST"])
def login():
    if session.get('username'):
        return redirect("/")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.CheckLogin(username, password)
        if user:
            session["id"] = user["id"]
            session["username"] = username
            return redirect("/")
        else:
            error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    if session.get('username'):
        return redirect("/")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.RegisterUser(username, password):
            return redirect("/")
        else:
            error = "Username already taken, please choose another"
    return render_template("register.html", error=error)

@app.route("/add", methods=["GET", "POST"])
def Add():
    if not session.get('username'):
        return redirect("/login")
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        duration = request.form['duration']
        distance = request.form['distance']
        supervisor = request.form['supervisor']
        time_of_day = request.form['time_of_day']
        db.AddSession(user_id, date, duration, distance, supervisor, time_of_day)
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:session_id>", methods=["GET", "POST"])
def Edit(session_id):
    if not session.get('username'):
        return redirect("/login")
    sessionData = db.GetSession(session_id, session['id'])
    if sessionData is None:
        return redirect("/")
    if request.method == "POST":
        date = request.form['date']
        duration = request.form['duration']
        distance = request.form['distance']
        supervisor = request.form['supervisor']
        time_of_day = request.form['time_of_day']
        db.EditSession(session_id, session['id'], date, duration, distance, supervisor, time_of_day)
        return redirect("/")
    return render_template("edit.html", session=sessionData)

@app.route("/delete/<int:session_id>", methods=["POST"])
def Delete(session_id):
    if not session.get('username'):
        return redirect("/login")
    db.DeleteSession(session_id, session['id'])
    return redirect("/")

app.run(debug=False, port=5000)