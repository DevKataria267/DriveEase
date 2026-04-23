from flask import Flask, render_template, request, redirect, session
import db

app = Flask(__name__)
app.secret_key = "driveease"

@app.route("/")
def Home():
    if not session.get('username'):
        return redirect("/register")
    sessionsData = db.GetAllSessions()
    return render_template("index.html", sessions=sessionsData)

@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        user = db.CheckLogin(username, password)
        if user:
            session["id"] = user["id"]
            session["username"] = username
            return redirect("/")
    return render_template("login.html")

@app.route("/logout")
def logout():
    session.clear()
    return redirect("/")

@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        if db.RegisterUser(username, password):
            return redirect("/")
    return render_template("register.html")

@app.route("/add", methods=["GET", "POST"])
def Add():
    if session.get('username') == None:
        return redirect("/")
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

app.run(debug=True, port=5000)