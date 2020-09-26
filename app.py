from flask import Flask, render_template, request, jsonify
import flask
from db import *

app = Flask(__name__)

react_cors_headers = {"Access-Control-Allow-Origin":"*", "Access-Control-Allow-Methods":"POST, GET, OPTIONS", "Access-Control-Allow-Headers":"X-PINGOTHER, Content-Type"}

@app.route("/", methods=['GET', 'POST'])
def index():
    return "post"

@app.route("/api/login", methods=['GET', 'POST', 'OPTIONS'])
def login():
    data = request.get_json()
    response = {}

    print(data)

    if request.method == "POST":
        email, password = data['email'], data['password']

        if emailExist(email):
            if isPassword(email, password):
                response['status'] = "ok"
                return jsonify(response), 200
            
            elif not isPassword(email, password):
                response['status'] = "Incorrect password!"
                return jsonify(response), 200

        elif not emailExist(email):
            response['status'] = "Email does not exist!"
            return jsonify(response), 404, {"Access-Control-Allow-Origin":"*"}

        
        return jsonify({"status":"server error"})

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/signup", methods=['GET', 'POST', 'OPTIONS'])
def signup():
    data = request.get_json()
    print(data)

    if request.method == "POST":
        email, username, first_name, last_name, password, confirm_password = data['email'], data['username'], data['first_name'], data['last_name'], data['password'], data['confirm_password']

        if not emailExist(email):
            if not usernameExist(username):
                if password == confirm_password:
                    add_user(email, username, first_name, last_name, password)
                    return jsonify({"status":"success"}), 200

                elif password != confirm_password:
                    return jsonify({"status":"Passwords do not match!"}), 200

            elif usernameExist(username):
                return jsonify({"status":"username already exists"}), 404

        elif emailExist(email):
            return jsonify({"status":"Email already exists!"}), 404

        return jsonify({"status":"server error"}), 500

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/hackathon/add", methods=['GET', 'POST', 'OPTIONS'])
def hackathon_add():
    data = request.get_json()

    print(data)

    if request.method == "POST":
        hackathon_name, hackathon_information, hackathon_email = data['hackathon_name'], data['hackathon_information'], data['hackathon_email']
        
        if not hackathon_email_exists(hackathon_email):
            add_hackathon(hackathon_name, hackathon_information, hackathon_email)
            return jsonify({"status":"success"}), 200

        elif hackathon_email_exists(hackathon_email):
            return jsonify({"status":"This contact mail already exists!"}), 403

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/hackathon/list", methods=['GET', 'POST', 'OPTIONS'])
def hackathon_list():
    if request.method == "GET":
        hackathons = listHackathons()
        hackathon_dicts = []

        for hackathon in hackathons:
            hackathon_dict = {"hackathon_id":hackathon[0], "hackathon_name":hackathon[1], "hackathon_information":hackathon[2], "hackathon_email":hackathon[3]}
            hackathon_dicts.append(hackathon_dict)

        return jsonify(hackathon_dicts), 200, react_cors_headers

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/hackathon/info/<hackathon_id>", methods=['GET', 'POST', 'OPTIONS'])
def hackathon_info(hackathon_id):

    if request.method == "GET":

        hackathon_name, hackathon_email, hackathon_info = getHackathonName(hackathon_id), getHackathonEmail(hackathon_id), getHackathonInformation(hackathon_id)

        return jsonify({"hackathon_name":hackathon_name, "hackathon_email":hackathon_email, "hackathon_info":hackathon_info}), 200, react_cors_headers


    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/teams/create/<hackathon_id>", methods=['GET', 'POST', 'OPTIONS'])
"""
POST /api/teams/create/{hackathon_id}

JSON PARAMS:
    team_name,
    team_information,
    team_discord_link

"""
def team_create(hackathon_id):
    if request.method == "POST":
        data = request.get_json()
        team_name, team_information, team_discord_link = data['team_name'], data['team_information'], data['team_discord_link']

        createTeam(hackathon_id, team_name, team_information, team_discord_link)

        return jsonify({"status":"success"}), 200, react_cors_headers

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/teams/delete/<hackathon_id>/<team_id>", methods=['GET', 'POST', 'OPTIONS'])
def delete_team(hackathon_id, team_id):
    if request.method == "GET":
        deleteTeam(hackathon_id, team_id)

        return jsonify({"status":"success"}), 200, react_cors_headers

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


@app.route("/api/teams/<hackathon_id>", methods=['GET', 'POST', 'OPTIONS'])
def hackathon_teams(hackathon_id):

    if request.method == "GET":
        teams = getTeamsFromHackathonId(hackathon_id)

        return jsonify(teams), 200, react_cors_headers

    elif request.method == "OPTIONS":
        return "", 204, react_cors_headers


    


if __name__ == '__main__':
    app.run() 