from flask import render_template, request, redirect, url_for, make_response, jsonify
from flask_login import current_user

from .forms import LoginForm
from .database import session
from werkzeug.security import check_password_hash, generate_password_hash

from .db_controls import add_new_item, get_events_by
from .database import User, Event
from . import app


@app.route("/create_event", methods=["POST"])
def create_event():
    data_from_request = request.get_json()
    data_from_request["user"] = current_user.id
    event = Event(**data_from_request)
    add_new_item(event)
    response = make_response()
    response.status_code = 200
    return response


@app.route("/get_events_by_date/<date>", methods=["POST"])
def get_events_by_date(date):
    data = {"name": "John", "age": 30}
    response = make_response(jsonify(data))
    response.headers.add('Access-Control-Allow-Origin', '*')
    response.headers.add('Access-Control-Allow-Methods', 'GET')
    response.headers.add('Access-Control-Allow-Headers', '*')
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


@app.route("/signup", methods=["POST", "GET"])
def signup():

    if request.method == "POST":

        nickname = request.form["nickname"]
        email = request.form["email"]
        password = request.form["password"]

        user = session.query(User).where(User.nickname == nickname).first()
        print(user)

        if user:
            return redirect(url_for("signup"))

        new_user = User(nickname=nickname, email=email, password=generate_password_hash(password))
        print(new_user)
        session.add(new_user)
        session.commit()
        session.close()
    return render_template("signup.html")


@app.route("/login", methods=["POST", "GET"] )
def login():
    form = LoginForm
    if request.method == "POST":
        nickname = request.form["nickname"]
        password = request.form["password"]

        remember = True if request.form.get("remember") else False

        user = session.query(User).where(User.nickname == nickname).first()
        print(user)
        print(check_password_hash(user.password, password))
        if not user or not check_password_hash(user.password, password):
            return redirect(url_for("login"))
        return redirect("/main")
    return render_template("login.html", form=form)
