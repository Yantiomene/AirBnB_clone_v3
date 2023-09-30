#!/usr/bin/python3
"""Handle all default API Action on User objects"""
from api.v1.views import app_views
from flask import jsonify, abort, make_response, request
from models import storage
from models.user import User


@app_views.route('/users', methods=['GET'], strict_slashes=False)
@app_views.route('/users/<user_id>', methods=['GET'], strict_slashes=False)
def get_users(user_id=None):
    """Retrieves all users objects"""
    if not user_id:
        return jsonify([user.to_dict() for user in
                        storage.all(User).values()])
    user = storage.get("User", user_id)
    if not user:
        abort(404)
    return jsonify(user.to_dict())


@app_views.route('/users/<user_id>', methods=['DELETE'],
                 strict_slashes=False)
def del_user(user_id):
    """Delete a user"""
    user = storage.get('User', user_id)
    if not user:
        abort(404)
    user.delete()
    storage.save()
    return make_response(jsonify({}), 200)


@app_views.route('/users', methods=['POST'], strict_slashes=False)
def create_user():
    """Create a user"""
    body = request.get_json()
    if not body:
        abort(400, "Not a json")

    if 'email' not in body:
        abort(400, "Missing email")

    if 'password' not in body:
        abort(400, "Missing password")

    user = User(**body)
    storage.new(user)
    storage.save()
    return make_response(jsonify(user.to_dict()), 201)


@app_views.route('/users/<user_id>', methods=['PUT'], strict_slashes=False)
def update_user(user_id):
    """Updates a User"""
    user = storage.get("User", user_id)
    if not user:
        abort(404)

    body = request.get_json()
    if not body:
        abort(400, "Not a JSON")

    for k, v in body.items():
        if k not in ['id', 'created_at', 'updated_at', 'email']:
            setattr(user, k, v)

    storage.save()
    return make_response(jsonify(user.to_dict()), 200)
