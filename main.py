import sqlite3
from werkzeug.security import generate_password_hash, check_password_hash

def GetDB():
    db = sqlite3.connect(".database/driveeasease.db")
    db.row_factory = sqlite3.Row
    return db

def GetAllSessions():
    db = GetDB()
    sessions = db.execute("SELECT * FROM Sessions").fetchall()
    db.close()
    return sessions