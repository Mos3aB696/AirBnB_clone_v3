#!/usr/bin/python3
"""
    The Python code defines routes for CRUD operations
    on Amenity objects using Flask and SQLAlchemy.
    :return: The code provided is a Flask API for managing
    Amenity objects. It includes routes for retrieving a list of
    all amenities, retrieving a specific amenity by ID, deleting an amenity,
    creating a new amenity, and updating an existing amenity.
"""


from flask import jsonify, abort, request, make_response
from models import storage
from models.state import State
from api.v1.views import app_views
from models.amenity import Amenity


@app_views.route('/amenities', methods=["GET"], strict_slashes=False)
def get_amenities():
    """
    Retrieve a list of all Amenity objects.
    """
    amenities = storage.all(Amenity)
    list_amenities = []
    for amenity in amenities.values():
        list_amenities.append(amenity.to_dict())
    return jsonify(list_amenities)


@app_views.route('/amenities/<amenity_id>', methods=["GET"],
                 strict_slashes=False)
def get_amenity(amenity_id):
    """
    Retrieve a Amenity object.
    """
    Amenit = storage.get(Amenity, amenity_id)
    if Amenit is None:
        abort(404)
    return jsonify(Amenit.to_dict())


@app_views.route('/amenities/<amenity_id>', methods=["DELETE"],
                 strict_slashes=False)
def delete_amenity(amenity_id):
    """
    Delete a Amenity object.
    """
    Amenit = storage.get(Amenity, amenity_id)
    if Amenit is None:
        abort(404)
    Amenit.delete()
    storage.save()
    return jsonify({})


@app_views.route('/amenities', methods=["POST"], strict_slashes=False)
def create_amenity():
    """
    Create a Amenity object.
    """
    if not request.json:
        abort(400, 'Not a JSON')
    if 'name' not in request.json:
        abort(400, 'Missing name')
    amenity = Amenity(**request.get_json())
    amenity.save()
    return make_response(jsonify(amenity.to_dict()), 201)


@app_views.route('/amenities/<amenity_id>', methods=["PUT"],
                 strict_slashes=False)
def update_amenity(amenity_id):
    """
    Update a Amenity object.
    """
    amenity = storage.get(Amenity, amenity_id)
    if amenity is None:
        abort(404)
    if not request.json:
        abort(400, 'Not a JSON')
    for key, value in request.get_json().items():
        if key not in ["id", "created_at", "updated_at"]:
            setattr(amenity, key, value)
    amenity.save()
    return jsonify(amenity.to_dict())


if __name__ == '__main__':
    pass
