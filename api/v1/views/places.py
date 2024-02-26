#!/usr/bin/python3
"""
Create a new view for Place objects that handles all
default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.city import City
from models.place import Place
from models.user import User


@app_views.route("cities/<city_id>/places", methods=["GET"],
                 strict_slashes=False)
def get_places(city_id):
    """
    get cities by id
    """
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    all_places = []
    for place in city.places:
        all_places.append(place.to_dict())
    return jsonify(all_places)


@app_views.route("/places/<place_id>", methods=["GET"],
                 strict_slashes=False)
def get_place(place_id):
    """
    Get place by id.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    return jsonify(place.to_dict())


@app_views.route("/places/<place_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_place(place_id):
    """
    Delete place by id.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    place.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("cities/<city_id>/places", methods=["POST"],
                 strict_slashes=False)
def create_place(city_id):
    """
    Create place.
    """
    dictionary = request.get_json()
    city = storage.get(City, city_id)
    if city is None:
        abort(404)
    if dictionary is None:
        abort(400, "Not a JSON")
    if "user_id" not in dictionary:
        abort(400, "Missing user_id")
    if storage.get(User, dictionary["user_id"]) is None:
        abort(404)
    if "name" not in dictionary:
        abort(400, "Missing name")
    dictionary["city_id"] = city_id
    place = Place(**dictionary)
    place.save()
    return make_response(jsonify(place.to_dict()), 201)


@app_views.route("/places/<place_id>", methods=["PUT"],
                 strict_slashes=False)
def modify_place(place_id):
    """
    Modify the place obj.
    """
    place = storage.get(Place, place_id)
    dictionary = request.get_json()
    if place is None:
        abort(404)
    if dictionary is None:
        abort(400, "Not a JSON")
    ignored_key = ["id", "user_id", "city_id", "created_at", "updated_at"]
    for key, value in dictionary.items():
        if key not in ignored_key:
            setattr(place, key, value)
    place.save()
    return make_response(jsonify(place.to_dict()), 200)

