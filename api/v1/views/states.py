#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort
from models import storage
app = Flask(__name__)


@app_views.route('/states', methods=['GET'])
def get_states():
    return jsonify(storage.all('State').values())

@app_views.route('/states/state_id', methods=['GET'])
def get_id(id=None):
    state_dict = storage.all(State)
    try:
        return jsonify(state_dict['State' + "." + id].to_dict())
    except:
        abort(404)
