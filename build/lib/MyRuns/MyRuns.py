# -*- coding: utf-8 -*-
from flask_sqlalchemy import SQLAlchemy
from stravalib.client import Client
from flask import Flask, redirect, render_template, url_for, request, flash, session
from sqlalchemy.sql import exists
from flask_login import LoginManager, UserMixin, login_user
import sqlite3
import datetime
import sys
import os

file_dir = os.path.dirname(__file__)
sys.path.append(file_dir)

from config_operations import ConfigFile, home


# config
def get_config():
    MY_STRAVA_CLIENT_ID = ConfigFile(home, 'config.yaml').read_parameter('MY_STRAVA_CLIENT_ID')
    MY_STRAVA_SECRET = ConfigFile(home, 'config.yaml').read_parameter('MY_STRAVA_SECRET')
    REDIRECT_URI = ConfigFile(home, 'config.yaml').read_parameter('REDIRECT_URI')
    SECRET_KEY = ConfigFile(home, 'config.yaml').read_parameter('SECRET_KEY')
    DATABASE = ConfigFile(home, 'db_address.yaml').read_parameter('DB_ADDRESS')

    user_token = sqlite3.connect(os.path.join(home, 'user_token.db'))

    access_token = None

    config_parameters = {'MY_STRAVA_SECRET': MY_STRAVA_SECRET, 'MY_STRAVA_CLIENT_ID': MY_STRAVA_CLIENT_ID,
                         'REDIRECT_URI': REDIRECT_URI, 'SECRET_KEY': SECRET_KEY, 'DATABASE': DATABASE,
                         'user_token': user_token, 'access_token': access_token}

    return config_parameters


def create_app():
    app = Flask(__name__)
    app.secret_key = get_config()['SECRET_KEY']
    app.config['SQLALCHEMY_DATABASE_URI'] = get_config()['DATABASE']
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
    return app

app = create_app()
db = SQLAlchemy()
strava_client = Client()


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(256))
    user_id = db.Column(db.Integer)
    access_token = db.Column(db.String(256))
    cookies = db.Column(db.String(256))


# setup login manager
login_manager = LoginManager()
login_manager.login_view = 'users.login'


@login_manager.user_loader
def load_user(user_token):
    return User.query.get(str(user_token))


# get the distance of run activities for the week from Monday to Sunday
def distance_for_week(monday_of_week):
    total_m_current_week = 0
    for activity in strava_client.get_activities(after=str(monday_of_week), before=str(monday_of_week + datetime.timedelta(days=7))):
        if activity.type == 'Run':
            total_m_current_week += int(activity.distance)

    return total_m_current_week


# calculate monday of current week
def monday():
    today = datetime.date.today()
    monday_of_current_week = today + datetime.timedelta(days=-today.weekday())
    return monday_of_current_week


@app.route('/authorize')
def authorize():
    code = request.args.get('code')
    MY_STRAVA_CLIENT_ID = get_config()['MY_STRAVA_CLIENT_ID']
    MY_STRAVA_SECRET = get_config()['MY_STRAVA_SECRET']
    access_token = strava_client.exchange_code_for_token(client_id=MY_STRAVA_CLIENT_ID,
                                                         client_secret=MY_STRAVA_SECRET,
                                                         code=code)
    if not access_token:
        flash('failed to login')
        return

    try:
        cookies = session['_id']
    except:
        cookies = None

    athlete = strava_client.get_athlete()
    user_token = User(user_id=athlete.id, username=athlete.firstname, access_token=access_token, cookies=cookies)
    user_cookies = db.session.query(User).get(athlete.id)

    user_exists = db.session.query(exists().where(User.user_id == athlete.id)).scalar()

    if not user_exists:
        db.session.add(user_token)
        db.session.commit()

    login_user(user_token)
    session['logged_in'] = True
    flash('Successfully signed in with Strava')
    return redirect(url_for('stats'))


@app.route('/')
def index():
    MY_STRAVA_CLIENT_ID = get_config()['MY_STRAVA_CLIENT_ID']
    REDIRECT_URI = get_config()['REDIRECT_URI']
    try:
        if session['logged_in']:
            authorize_url = strava_client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                                                            redirect_uri=REDIRECT_URI)
            return redirect(authorize_url)

    except:
        print('not logged in')
        authorize_url = strava_client.authorization_url(client_id=MY_STRAVA_CLIENT_ID,
                                                        redirect_uri=REDIRECT_URI)
        return render_template('index.html', authorize_url=authorize_url)


@app.route('/stats')
def stats():
    # This block redirects the user to index if he wasn't authorized
    try:
        athlete = strava_client.get_athlete()
    except:
        return redirect(url_for('index'))

    # total distance for current week
    total_m_current_week = distance_for_week(monday())

    # set target for the current week based on previous week + 10%
    target_m_per_week = round(distance_for_week(monday() - datetime.timedelta(days=7)) * 1.1)
    target_km_per_week = round(target_m_per_week / 1000, 1)

    # calculation of progress for progress bar in percents
    try:
        progress = round(total_m_current_week / target_m_per_week * 100)
    except ZeroDivisionError:
        progress = 0
        target_km_per_week = 5
    return render_template('stats.html', target_km_per_week=target_km_per_week, progress=progress)

# hook up extensions to app
db.init_app(app)
login_manager.init_app(app)


if __name__ == "__main__":
    app = create_app()
    app.run()
