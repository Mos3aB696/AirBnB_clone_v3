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
from models import Amenity
from models import State


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


# New endpoint: POST /api/v1/places_search
@app_views.route('/places_search', methods=['POST'],
                 strict_slashes=False)
def places_search():
    """
    Retrieves Place objects based on the provided JSON search criteria
    """

    if request.get_json() is None:
        abort(400, description="Not a JSON")

    data = request.get_json()

    if data and len(data):
        states = data.get('states', None)
        cities = data.get('cities', None)
        amenities = data.get('amenities', None)

    if not data or not len(data) or (
            not states and
            not cities and
            not amenities):
        places = storage.all(Place).values()
        list_places = []
        for place in places:
            list_places.append(place.to_dict())
        return jsonify(list_places)

    list_places = []

    if states:
        states_obj = [storage.get(State, s_id) for s_id in states]
        for state in states_obj:
            if state:
                for city in state.cities:
                    if city:
                        for place in city.places:
                            list_places.append(place)

    if cities:
        city_obj = [storage.get(City, c_id) for c_id in cities]
        for city in city_obj:
            if city:
                for place in city.places:
                    if place not in list_places:
                        list_places.append(place)

    if amenities:
        if not list_places:
            list_places = storage.all(Place).values()
        amenities_obj = [storage.get(Amenity, a_id) for a_id in amenities]

        list_places = [place for place in list_places
                       if all([am in place.amenities
                               for am in amenities_obj])]

    places = []
    for i in list_places:
        j = i.to_dict()
        j.pop('amenities', None)
        places.append(j)

    return jsonify(places)
