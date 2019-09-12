#!/usr/bin/python3
"""script that starts a Flask web application"""

from flask import Flask, jsonify, abort, request
from models import storage
from api.v1.views import app_views
from models.amenity import Amenity
from models.place import Place
import os
app = Flask(__name__)


@app_views.route('/places/<place_id>/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenity_for_place(place_id=None):
    """Retrieves the list of all Amenity objects for a place"""
    place_object = storage.get("Place", place_id)
    if place_object is None:
        return jsonify({}), 404
    amenities_list = []
    for amenity in place_object.amenities:
        amenities_list.append(amenity.to_dict())
    return jsonify(amenities_list), 200


@app_views.route('/amenities/<amenity_id>',
                 methods=['DELETE'], strict_slashes=False)
def delete_amenity_to_place(amenity_id=None):
    """Deletes a Amenity object"""
    obj = storage.get('Amenity', amenity_id)
    if obj is None:
        abort(404)
    else:
        storage.delete(obj)
        storage.save()
    return jsonify({}), 200


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity_to_place():
    """Creates a Amenity"""
    result = request.get_json()
    if not result:
        abort(400, {"Not a JSON"})
    if 'name' not in result:
        abort(400, {"Missing name"})
    obj = Amenity(name=result['name'])
    storage.new(obj)
    storage.save()
    return jsonify(obj.to_dict()), 201
