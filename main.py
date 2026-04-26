from flask import Flask, render_template, request, redirect, session
from dotenv import load_dotenv
import os
import db

load_dotenv()

app = Flask(__name__)
# secret key from .env so it's not hardcoded
app.secret_key = os.getenv("SECRET_KEY")

@app.route("/")
def Home():
    # kick user to login if they're not logged in
    if not session.get('username'):
        return redirect("/login")
    # only get sessions for the logged in user
    sessionsData = db.GetAllSessions(session['id'])
    return render_template("index.html", sessions=sessionsData)

@app.route("/login", methods=["GET", "POST"])
def login():
    # if already logged in just go home
    if session.get('username'):
        return redirect("/")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # stop people putting in massive inputs
        if len(username) > 50 or len(password) > 50:
            error = "Input too long"
        else:
            # check username and password against db
            user = db.CheckLogin(username, password)
            if user:
                # save user info to session
                session["id"] = user["id"]
                session["username"] = username
                return redirect("/")
            else:
                error = "Invalid username or password"
    return render_template("login.html", error=error)

@app.route("/logout")
def logout():
    # wipe the session and go back to login
    session.clear()
    return redirect("/login")

@app.route("/register", methods=["GET", "POST"])
def register():
    # if already logged in just go home
    if session.get('username'):
        return redirect("/")
    error = None
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        # check inputs arent too long
        if len(username) > 50 or len(password) > 50:
            error = "Input too long"
        # username needs to be at least 3 chars
        elif len(username) < 3:
            error = "Username must be at least 3 characters"
        # password needs to be at least 6 chars
        elif len(password) < 6:
            error = "Password must be at least 6 characters"
        else:
            if db.RegisterUser(username, password):
                return redirect("/")
            else:
                error = "Username already taken, please choose another"
    return render_template("register.html", error=error)

@app.route("/add", methods=["GET", "POST"])
def Add():
    # not logged in? go to login
    if not session.get('username'):
        return redirect("/login")
    if request.method == "POST":
        user_id = session['id']
        date = request.form['date']
        duration = request.form['duration']
        distance = request.form['distance']
        supervisor = request.form['supervisor']
        time_of_day = request.form['time_of_day']
        # make sure nothing is left empty
        if not date or not duration or not distance or not supervisor:
            return render_template("add.html", error="All fields are required")
        # check inputs arent too long
        if len(duration) > 50 or len(supervisor) > 50:
            return render_template("add.html", error="Input too long")
        db.AddSession(user_id, date, duration, distance, supervisor, time_of_day)
        return redirect("/")
    return render_template("add.html")

@app.route("/edit/<int:session_id>", methods=["GET", "POST"])
def Edit(session_id):
    # not logged in? go to login
    if not session.get('username'):
        return redirect("/login")
    # get the session and make sure it belongs to this user
    sessionData = db.GetSession(session_id, session['id'])
    # if it doesnt exist or belongs to someone else, go home
    if sessionData is None:
        return redirect("/")
    if request.method == "POST":
        date = request.form['date']
        duration = request.form['duration']
        distance = request.form['distance']
        supervisor = request.form['supervisor']
        time_of_day = request.form['time_of_day']
        # make sure nothing is left empty
        if not date or not duration or not distance or not supervisor:
            return render_template("edit.html", session=sessionData, error="All fields are required")
        # check inputs arent too long
        if len(duration) > 50 or len(supervisor) > 50:
            return render_template("edit.html", session=sessionData, error="Input too long")
        db.EditSession(session_id, session['id'], date, duration, distance, supervisor, time_of_day)
        return redirect("/")
    return render_template("edit.html", session=sessionData)

@app.route("/delete/<int:session_id>", methods=["POST"])
def Delete(session_id):
    # not logged in? go to login
    if not session.get('username'):
        return redirect("/login")
    # the AND user_id in the sql means you can only delete your own sessions
    db.DeleteSession(session_id, session['id'])
    return redirect("/")

app.run(debug=False, port=5000)