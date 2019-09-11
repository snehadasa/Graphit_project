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
def get_state(state_id=None):
    state_dict = storage.all('State')
    try:
        return jsonify(state_dict['State' + "." + state_id].to_dict())
    except:
        abort(404)


@app_views.route('/states/<state_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_state(state_id=None):
    try:
        obj = storage.get('State', state_id)
        storage.delete(obj)
        storage.save()
    except:
        abort(404)
    return jsonify({}), 200


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def post_state():
    result = request.get_json()
    if not result:
        abort(400, {"message": "Not a JSON"})
    if 'name' not in result:
        abort(400, {"message": "Missing name"})
    obj = State(name=result['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201


@app_views.route('/states/<state_id>', methods=['PUT'], strict_slashes=False)
def put_state(state_id=None):
    result = request.get_json()
    if not result:
        abort(400, {"message": "Not a JSON"})
    obj = storage.get('State', state_id)
    if obj is None:
        abort(404)
    for key, value in result.items():
        if key != "id" and "created_at" and "updated_at":
            setattr(obj, key, value)
    storage.save()
    return jsonify(obj.to_dict()), 200

if __name__ == "__main__":
    app.run(host='0.0.0.0', port=5000)
