#!/usr/bin/python3
"""Hanldes default API actions on State objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.state import State


@app_views.route('/states', methods=['GET'], strict_slashes=False)
@app_views.route('/states/<state_id>', methods=['GET'], strict_slashes=False)
def get_states(state_id=None):
    """Retrieves the list of all states objects
    Or a state object base on his id
    """
    if not state_id:
        return jsonify([state.to_dict() for state in
                        storage.all(State).values()])
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    return jsonify((state.to_dict()))


@app_views.route('/states/<state_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_state(state_id):
    """Deletes a state Object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)
    state.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/states', methods=['POST'], strict_slashes=False)
def create_state():
    """Create a state"""
    state_dic = request.get_json()
    if not state_dic:
        abort(400, "Not a JSON")
    if "name" not in state_dic:
        abort(400, "Missing name")
    state = State(**state_dic)
    storage.new(state)
    storage.save()
    return make_response(jsonify(state.to_dict()), 201)


@app_views.route('states/<state_id>', methods=['PUT'], strict_slashes=False)
def update_state(state_id):
    """Update a State object"""
    state = storage.get("State", state_id)
    if not state:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    for k, v in body.items():
        if k != 'id' and k != 'created_at' and k != 'updated_at':
            setattr(state, k, v)

    storage.save()
    return make_response(jsonify(state.to_dict()), 200)
