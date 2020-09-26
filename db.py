import sqlite3
from hashlib import md5
import uuid
from ast import literal_eval

def hashed(password):
    return md5(password.encode()).hexdigest()


def add_user(email, username, first_name, last_name, password):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    password = hashed(password)

    conn.execute("INSERT INTO users VALUES(?, ?, ?, ?, ?)", (email, username, first_name, last_name, password,))
    db.commit()
    conn.close()

def isPassword(email, password):
    db = sqlite3.connect("database.db")
    conn = db.cursor()
    hashed_password = hashed(password)

    conn.execute("SELECT password FROM users WHERE email=?", (email,))
    
    password = conn.fetchone()[0]
    db.commit()
    conn.close()

    return password == hashed_password

def emailExist(email):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT email FROM users WHERE email=?", (email,))
    email = conn.fetchone()

    db.commit()
    conn.close()

    if email:
        return True
    
    return False


def usernameExist(username):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT username FROM users WHERE username=?", (username,))
    username_exist = conn.fetchone()

    db.commit()
    conn.close()

    if username_exist:
        return True
    
    return False


def add_hackathon(name, information, owner_email):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    hackathon_id = uuid.uuid4().hex
    conn.execute("INSERT INTO hackathons VALUES(?, ?, ?, ?, ?)", (hackathon_id, name, information, owner_email, "[]",))
    db.commit()
    conn.close()


def deleteHackathon(hackathon_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("DELETE FROM hackathons WHERE id=?", (hackathon_id,))
    db.commit()
    conn.close()


def getHackathonInformation(hackathon_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT information FROM hackathons WHERE id=?", (hackathon_id,))
    hackathon_information = conn.fetchone()[0]
    db.commit()
    conn.close()

    return hackathon_information


def getHackathonEmail(hackathon_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT owner_email FROM hackathons WHERE id=?", (hackathon_id,))
    owner_email = conn.fetchone()[0]

    db.commit()
    conn.close()

    return owner_email


def getHackathonName(hackathon_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT name FROM hackathons WHERE id=?", (hackathon_id,))
    hackathon_name = conn.fetchone()[0]

    db.commit()
    conn.close()

    return hackathon_name


def hackathon_email_exists(hackathon_email):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT owner_email FROM hackathons WHERE owner_email=?", (hackathon_email,))
    hackathon_email = conn.fetchone()

    if hackathon_email:
        return True

    return False

def listHackathons():
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT * FROM hackathons")
    hackathons = conn.fetchall()

    db.commit()
    conn.close()

    return hackathons


def getTeamsFromHackathonId(hackathon_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    conn.execute("SELECT teams FROM hackathons WHERE id=?", (hackathon_id,))
    teams = literal_eval(conn.fetchone()[0])

    db.commit()
    conn.close()

    return teams


def createTeam(hackathon_id, team_name, team_information, team_discord_link):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    teams = getTeamsFromHackathonId(hackathon_id)
    team_id = uuid.uuid4().hex
    team_dict = {"team_id":team_id, "team_name":team_name, "team_information":team_information, "team_discord_link":team_discord_link, "team_members":[]}
    teams.append(team_dict)

    conn.execute("UPDATE hackathons SET teams=? WHERE id=?", (str(teams), hackathon_id,))
    db.commit()
    conn.close()


def deleteTeam(hackathon_id, team_id):
    db = sqlite3.connect("database.db")
    conn = db.cursor()

    teams = getTeamsFromHackathonId(hackathon_id)

    for team in teams:
        if team["team_id"] == team_id:
            teams.remove(team)

    conn.execute("UPDATE hackathons SET teams=? WHERE id=?", (str(teams), hackathon_id,))
    db.commit()
    conn.close()
    

