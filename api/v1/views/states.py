#!/usr/bin/python3
"""script that starts a Flask web application"""


from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.state import State
app = Flask(__name__)


@app_views.route('/states', methods=['GET'], strict_slashes=False)
def get_states():
    states = storage.all('State')
    state_list = []
    for state in states.values():
        state_list.append(state.to_dict())
    return jsonify(state_list)

@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_id(state_id=None):
    state_dict = storage.all('State')
    try:
        return jsonify(state_dict['State' + "." + state_id].to_dict())
    except:
        abort(404)

@app_views.route('/states/<state_id>', methods=['DELETE'], strict_slashes=False)
def delete_id(state_id=None):
    try:
        obj = storage.get('State', state_id)
        storage.delete(obj)
        storage.save()
    except:
        abort(404)
    return jsonify({}), 200

@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_states():
    result = request.get_json()
    if not result:
        abort(400, {"message": "Not a JSON"})
    if not 'name' in result:
        abort(400, {"message": "Missing name"})
    obj = State(name = result['name'])
    storage.save()
    return jsonify(obj.to_dict()), 201
