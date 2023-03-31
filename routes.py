from flask import render_template, request, redirect, url_for, make_response, jsonify
from .database import session
from werkzeug.security import check_password_hash, generate_password_hash
from .db_controls import add_new_item, get_events_by, delete_user
from .database import User, Event
from . import app
from datetime import timedelta
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity


def add_event_to_database(event_data):
    print(event_data)
    event_data["user"] = 1
    event = Event(**event_data)
    add_new_item(event)


def create_response(status_code):
    response = make_response()
    response.status_code = status_code
    return response


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    print(data_from_request)
    try:
        add_event_to_database(data_from_request)
        response = create_response({"isAdded": True})
        response.status_code = 200
    except Exception as e:
        print(e)
        response = create_response({"isAdded": False, "exception": e})
        response.status_code = 500
    return response


@app.route("/get_events_by_date/<date>", methods=["GET"])
def get_events_by_date(date):
    print(date[:10])
    data = get_events_by(date[:10])
    response = make_response(jsonify(data))
    return response


@app.route("/")
@app.route("/main")
def index():
    return render_template("main.html")


@app.route("/test")
def test():
    import requests

    response = requests.get('https://www.boredapi.com/api/activity')
    print(response)
    if response.status_code == 200:
        data = response.json()["activity"]
    else:
        data = "ERROR"

    return render_template("main.html", data=data)


@app.errorhandler(404)
@app.errorhandler(500)
@app.errorhandler(405)
def handle_error(e):
    return render_template("custom_error.html", error=e.code)


@app.route("/signup", methods=["GET", "POST"])
def signup():
    data_from_request = request.get_json()
    name = data_from_request["nickname"]

    user_check = session.query(User).where(User.nickname == name).first()

    if user_check:
        response = make_response(jsonify({"isRegistered": False, "reason": "userExists"}), 409)
        return response

    data_from_request["password"] = generate_password_hash(data_from_request["password"])
    new_user = User(**data_from_request)
    add_new_item(new_user)
    response = make_response(jsonify({"isRegistered": True}), 200)
    return response


@app.route("/login", methods=["POST"])
def login():
    data_from_request = request.get_json()

    name = data_from_request["nickname"]
    password = data_from_request["password"]

    user_check = session.query(User).where(User.nickname == name).first()

    if not user_check:
        print(name, password)
        response = make_response({"isLogged": False})
        return response

    if check_password_hash(user_check.password, password):
        print(name, password)
        token = create_access_token(identity=user_check.id, expires_delta=timedelta(days=30))
        print(token)
        response = make_response(jsonify({"isLogged": True, "token": token}), 200)
        print(response.date)
        return response

    response = make_response({"isLogged": False})
    return response


@app.route("/delete_user_by/<nickname>")
def delete_user_by(nickname):
    try:
        delete_user(nickname)
        response_json = {"isDeleted": True}
        status = 200
    except:
        response_json = {"isDeleted": False}
        status = 500

    response = make_response(response_json, status)
    return response




# @login_manager.user_loader
# def load_user(user):
#     return session.query(User).get(int(user))

