import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/driveease.db")
    db.row_factory = sqlite3.Row
    return db

def GetAllSessions():
    db = GetDB()
    sessions = db.execute("SELECT * FROM Sessions").fetchall()
    db.close()
    return sessions

def CheckLogin(username, password):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    if user is not None:
        if check_password_hash(user['password'], password):
            return user
    return None