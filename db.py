import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/driveease.db")
    db.row_factory = sqlite3.Row
    return db

def GetAllSessions(user_id):
    db = GetDB()
    sessions = db.execute("""SELECT Sessions.id, Sessions.date, Sessions.duration, Sessions.distance,
        Sessions.supervisor, Sessions.time_of_day, Users.username
        FROM Sessions JOIN Users ON Sessions.user_id = Users.id
        WHERE Sessions.user_id = ?
        ORDER BY date DESC""", (user_id,)).fetchall()
    db.close()
    return sessions

def GetSession(session_id, user_id):
    db = GetDB()
    session = db.execute("SELECT * FROM Sessions WHERE id=? AND user_id=?", (session_id, user_id,)).fetchone()
    db.close()
    return session

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
    try:
        db = GetDB()
        hash = generate_password_hash(password)
        db.execute("INSERT INTO Users(username, password) VALUES(?, ?)", (username, hash,))
        db.commit()
        return True
    except:
        return False

def AddSession(user_id, date, duration, distance, supervisor, time_of_day):
    if date is None or duration is None:
        return False
    db = GetDB()
    db.execute("INSERT INTO Sessions(user_id, date, duration, distance, supervisor, time_of_day) VALUES (?, ?, ?, ?, ?, ?)",
    (user_id, date, duration, distance, supervisor, time_of_day,))
    db.commit()
    return True

def EditSession(session_id, user_id, date, duration, distance, supervisor, time_of_day):
    db = GetDB()
    db.execute("""UPDATE Sessions SET date=?, duration=?, distance=?, supervisor=?, time_of_day=?
        WHERE id=? AND user_id=?""", (date, duration, distance, supervisor, time_of_day, session_id, user_id,))
    db.commit()
    return True

def DeleteSession(session_id, user_id):
    db = GetDB()
    db.execute("DELETE FROM Sessions WHERE id=? AND user_id=?", (session_id, user_id,))
    db.commit()
    return True