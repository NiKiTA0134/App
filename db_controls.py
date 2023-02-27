from flask import session, jsonify
from .database import User, Event


def add_new_item(obj):
    session.add()
    session.commit()


def check_if_user_exists(nickname: str):
    user = session.query(User).where(User.nickname == nickname).first
    return user


def get_events_by(date):
    events = session.query(Event).where(Event.date == date).all()
    response = jsonify({'events': [event.to_dict() for event in events]})
    return response