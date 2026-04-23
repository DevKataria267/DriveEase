import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/driveease.db")
    db.row_factory = sqlite3.Row
    return db

def GetAllSessions():
    db = GetDB()
    sessions = db.execute("""SELECT Sessions.date, Sessions.duration, Sessions.distance,
        Sessions.supervisor, Sessions.time_of_day, Users.username
        FROM Sessions JOIN Users ON Sessions.user_id = Users.id
        ORDER BY date DESC""").fetchall()
    db.close()
    return sessions

def CheckLogin(username, password):
    db = GetDB()
    user = db.execute("SELECT * FROM Users WHERE username=?", (username,)).fetchone()
    if user is not None:
        if check_password_hash(user['password'], password):
            return user
    return None

def RegisterUser(username, password):
    if username is None or password is None:
        return False
    db = GetDB()
    hash = generate_password_hash(password)
    db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
    db.commit()
    return True

def AddSession(user_id, date, duration, distance, supervisor, time_of_day):
    if date is None or duration is None:
        return False
    db = GetDB()
    db.execute("INSERT INTO Sessions(user_id, date, duration, distance, supervisor, time_of_day) VALUES (?, ?, ?, ?, ?, ?)",
    (user_id, date, duration, distance, supervisor, time_of_day,))
    db.commit()
    return True