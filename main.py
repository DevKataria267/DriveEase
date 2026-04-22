from flask import Flask, render_template, request
import db

app = Flask(__name__)
app.secret_key = "driveease"

@app.route("/")
def Home():
    sessionData = db.GetAllSessions()
    return render_template("index.html", sessions=sessionData)

@app.route("/login", methods=["GET", "POST"])
def Login():
    return render_template("login.html")

app.run(debug=True, port=5000)