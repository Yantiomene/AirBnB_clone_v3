#!/usr/bin/python3
"""Handles all default RESTFul API actions on City objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State
from models.city import City


@app_views.route('/states/<state_id>/cities', methods=['GET'],
                 strict_slashes=False)
def get_cities(state_id):
    """Retrieves all cities from a state"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify([city.to_dict() for city in state.cities])


@app_views.route('/cities/<city_id>', methods=['GET'], strict_slashes=False)
def get_city(city_id):
    """Retrieves a ctiy"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    return jsonify(city.to_dict())


@app_views.route('/cities/<city_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_city(city_id):
    """Deletes a city"""
    city = storage.get('City', city_id)
    if not city:
        abort(404)
    city.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states/<state_id>/cities', methods=['POST'],
                 strict_slashes=False)
def create_city(state_id):
    """Creates a city in a state"""
    state = storage.get('State', state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')
    if 'name' not in body:
        abort(400, 'Missing name')

    city = City(**body)
    setattr(city, 'state_id', state_id)
    storage.new(city)
    storage.save()
    return make_response(jsonify(city.to_dict()), 201)


@app_views.route('/cities/<city_id>', methods=['PUT'],
                 strict_slashes=False)
def update_city(city_id):
    """Updates a City object"""
    city = storage.get("City", city_id)
    if not city:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, 'Not a JSON')

    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at',
                     'state_id']:
            setattr(city, k, v)
    storage.save()

    return make_response(jsonify(city.to_dict()), 200)
