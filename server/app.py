#!/usr/bin/env python3

from flask import Flask, request, make_response
from flask_migrate import Migrate

from models import db, Episode, Guest, Appearance

app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///app.db'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.json.compact = False

migrate = Migrate(app, db)

db.init_app(app)

@app.route('/')
def home():
    return '<h1>Late Show Code Challenge</h1>'

@app.route('/episodes')
def episodes():
    episodes_dict_list = [epi.to_dict(rules=('-appearances', '-guests',)) for epi in Episode.query.all()]
    return episodes_dict_list

if __name__ == '__main__':
    app.run(port=5555, debug=True)

