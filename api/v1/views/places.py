#!/usr/bin/python3
"""Handles all default RESTFul API actions on Place objects"""

from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route('/cities/<string:city_id>/places', methods=['GET'],
                 strict_slashes=False)
def get_places(city_id):
    """retrieve all places in a specified city"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    places = []
    for place in city.places:
        places.append(place.to_dict())
    return jsonify(places)


@app_views.route('/places/<string:place_id>', methods=['GET'],
                 strict_slashes=False)
def get_place(place_id):
    """retrieve a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route('/places/<string:place_id>', methods=['DELETE'],
                 strict_slashes=False)
def delete_place(place_id):
    """deletes place based on its id"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return (jsonify({}))


@app_views.route('/cities/<string:city_id>/places', methods=['POST'],
                 strict_slashes=False)
def post_place(city_id):
    """create a new place"""
    city = storage.get("City", city_id)
    if city is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    kwargs = request.get_json()
    if 'user_id' not in kwargs:
        abort(400, 'Missing user_id')
    user = storage.get("User", kwargs['user_id'])
    if user is None:
        abort(404)
    if 'name' not in kwargs:
        abort(400, 'Missing name')
    kwargs['city_id'] = city_id
    place = Place(**kwargs)
    storage.new(place)
    storage.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route('/places/<string:place_id>', methods=['PUT'],
                 strict_slashes=False)
def put_place(place_id):
    """update a place"""
    place = storage.get("Place", place_id)
    if place is None:
        abort(404)
    if not request.get_json():
        abort(400, 'Not a JSON')
    for attr, val in request.get_json().items():
        if attr not in ['id', 'user_id', 'city_id', 'created_at',
                        'updated_at']:
            setattr(place, attr, val)
    storage.save()
    return jsonify(place.to_dict())


@app_views.route('/places_search', methods=['POST'], strict_slashes=False)
def post_places_search():
    """searches for a place"""
    if not request.get_json():
        abort(400, "Not a JSON")

    params = request.get_json()
    state_ids = params.get('states', [])
    city_ids = params.get('cities', [])
    amenity_ids = params.get('amenities', [])
    amenity_objects = []
    for amenity_id in amenity_ids:
        amenity = storage.get('Amenity', amenity_id)
        if amenity:
            amenity_objects.append(amenity)
    if state_ids == city_ids == []:
        places = storage.all('Place').values()
    else:
        places = []
        for state_id in state_ids:
            state = storage.get('State', state_id)
            state_cities = state.cities
            for city in state_cities:
                if city.id not in city_ids:
                    city_ids.append(city.id)
        for city_id in city_ids:
            city = storage.get('City', city_id)
            for place in city.places:
                places.append(place)
    verified_places = []
    for place in places:
        place_amenities = place.amenities
        verified_places.append(place.to_dict())
        for amenity in amenity_objects:
            if amenity not in place_amenities:
                verified_places.pop()
                break
    return jsonify(verified_places)
