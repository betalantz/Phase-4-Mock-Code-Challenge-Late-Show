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

@app.route('/episodes/<int:id>', methods=['GET', 'DELETE'])
def episode_by_id(id):
    episode = Episode.query.filter_by(id=id).first()
    if episode is None:
        body = {"error": "404: Episode not found"}
        res = make_response(body, 404)
        return res
    if request.method == 'GET':
        return episode.to_dict(rules=('-appearances', 'guests', '-guests.appearances'))
    if request.method == 'DELETE':
        db.session.delete(episode)
        db.session.commit()
        res = make_response("", 204)
        return res
    
@app.route('/guests')
def guests():
    guests_dict_list = [guest.to_dict() for guest in Guest.query.all()]
    return guests_dict_list

@app.route('/appearances', methods=['POST'])
def appearances():
    try:
        app_json = request.get_json()
        new_app = Appearance(
            rating=app_json['rating'],
            episode_id=app_json['episode_id'],
            guest_id=app_json['guest_id']
        )
    except ValueError:
        return make_response({"error": "400: Validation error"}, 400)
    
    db.session.add(new_app)
    db.session.commit()
    app_dict = new_app.to_dict(rules=('-episode_id', '-guest_id'))
    res = make_response(app_dict, 201)
    return res

if __name__ == '__main__':
    app.run(port=5555, debug=True)

