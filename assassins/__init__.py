import os
from flask import Flask, render_template, request, session, url_for, redirect, flash
from flask_sqlalchemy import SQLAlchemy
from datetime import datetime
from passlib.hash import sha256_crypt
import gc
from functools import wraps
from assigner import assignTargets

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://root@localhost/assassins'


db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column('id', db.Integer, primary_key=True)
    username = db.Column('username', db.Unicode)
    first_name = db.Column('first_name', db.Unicode)
    last_name = db.Column('last_name', db.Unicode)
    password = db.Column('password', db.Unicode)
    is_out = db.Column('is_out', db.Boolean)
    kills = db.Column('kills', db.Integer)

    def __init__(self, username, first_name, last_name,  password, is_out, kills):
        self.username = username
        self.first_name = first_name
        self.last_name = last_name
        self.password = password
        self.is_out = is_out
        self.kills = kills

class Hit(db.Model):
    __tablename__ = 'hits'

    id = db.Column('id', db.Integer, primary_key=True)
    a_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    prey_id = db.Column(db.Integer, db.ForeignKey('users.id'))
    a_uname = db.Column(db.Unicode, db.ForeignKey('users.username'))
    prey_uname = db.Column(db.Unicode, db.ForeignKey('users.username'))
    a_ver = db.Column('a_ver', db.Boolean)
    prey_ver = db.Column('prey_ver', db.Boolean)
    done = db.Column('done', db.Boolean)
    done_date = db.Column('done_date', db.DateTime)

    def __init__(self, a_id, prey_id, a_uname, prey_uname, a_ver, prey_ver, done, done_date):
        self.a_id = a_id
        self.prey_id = prey_id
        self.a_uname = a_uname
        self.prey_uname = prey_uname
        self.a_ver = a_ver
        self.prey_ver = prey_ver
        self.done = done
        self.done_date = done_date











def login_required(f):
    @wraps(f)
    def wrap(*args, **kwargs):
        if 'logged_in' in session:
            return f(*args, **kwargs)
        else:
            flash("You need to login first")
            return render_template('index.html', loginmodal_active=True)
    return wrap


import assassins.views
