#!/usr/bin/python3
"""Handles all default RESTFul API actions on Amenity objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.amenity import Amenity


@app_views.route('/amenities', methods=['GET'],
                 strict_slashes=False)
def get_amenities():
    """Retrieves all amenities"""
    amenities = []
    for amenity in storage.all("Amenity").values():
        amenities.append(amenity.to_dict())
    return jsonify(amenities)


@app_views.route('/amenities/<string:amenity_id>', methods=['GET'],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """Retrieves each amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    return jsonify(amenity.to_dict())


@app_views.route('/amenities/<string:amenity_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """deletes an amenity based on its id"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    amenity.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/amenities', methods=['POST'], strict_slashes=False)
def post_amenity():
    """create a new amenity"""
    if not request.get_json():
        abort(400, 'Not a JSON')
    if 'name' not in request.get_json():
        abort(400, 'Missing name')
    amenity = Amenity(**(request.get_json()))
    storage.new(amenity)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<string:amenity_id>', methods=['PUT'],
                 strict_slashes=False)
def put_amenity(amenity_id):
    """update an amenity"""
    amenity = storage.get("Amenity", amenity_id)
    if amenity is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for attr, val in request.get_json().items():
        if attr not in ['id', 'created_at', 'updated_at']:
            setattr(amenity, attr, val)
    storage.save()
    return make_response(jsonify(amenity.to_dict()), 200)
