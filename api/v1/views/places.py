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
from models.state import State
from models.amenity import Amenity
import os

STORAGE_TYPE = os.getenv('STORAGE_TYPE', 'default_value')


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


@app_views.route('/places_search', methods=['POST'])
def places_search():
    """
        places route to handle http method for request to search places
    """
    all_places = [p for p in storage.all('Place').values()]
    req_json = request.get_json()
    if req_json is None:
        abort(400, 'Not a JSON')
    states = req_json.get('states')
    if states and len(states) > 0:
        all_cities = storage.all('City')
        state_cities = set([city.id for city in all_cities.values()
                            if city.state_id in states])
    else:
        state_cities = set()
    cities = req_json.get('cities')
    if cities and len(cities) > 0:
        cities = set([
            c_id for c_id in cities if storage.get('City', c_id)])
        state_cities = state_cities.union(cities)
    amenities = req_json.get('amenities')
    if len(state_cities) > 0:
        all_places = [p for p in all_places if p.city_id in state_cities]
    elif amenities is None or len(amenities) == 0:
        result = [place.to_json() for place in all_places]
        return jsonify(result)
    places_amenities = []
    if amenities and len(amenities) > 0:
        amenities = set([
            a_id for a_id in amenities if storage.get('Amenity', a_id)])
        for p in all_places:
            p_amenities = None
            if STORAGE_TYPE == 'db' and p.amenities:
                p_amenities = [a.id for a in p.amenities]
            elif len(p.amenities) > 0:
                p_amenities = p.amenities
            if p_amenities and all([a in p_amenities for a in amenities]):
                places_amenities.append(p)
    else:
        places_amenities = all_places
    result = [place.to_json() for place in places_amenities]
    return jsonify(result)
