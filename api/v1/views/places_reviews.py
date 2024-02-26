#!/usr/bin/python3
"""
Create a new view for Review object that
handles all default RESTFul API actions.
"""
from api.v1.views import app_views
from flask import jsonify, abort, request, make_response
from models import storage
from models.place import Place
from models.review import Review
from models.user import User


@app_views.route("/places/<place_id>/reviews", methods=["GET"],
                 strict_slashes=False)
def get_reviews(place_id):
    """
    Get all reviews from Places object.
    """
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    reviews = []
    for review in place.reviews:
        reviews.append(review.to_dict())
    return jsonify(reviews)


@app_views.route("/reviews/<review_id>", methods=["GET"],
                 strict_slashes=False)
def get_review(review_id):
    """
    Get review by id.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    return jsonify(review.to_dict())


@app_views.route("/reviews/<review_id>", methods=["DELETE"],
                 strict_slashes=False)
def delete_review(review_id):
    """
    Delete review from storage.
    """
    review = storage.get(Review, review_id)
    if review is None:
        abort(404)
    review.delete()
    storage.save()
    return jsonify({}), 200


@app_views.route("/places/<place_id>/reviews", methods=["POST"],
                 strict_slashes=False)
def create_review(place_id):
    """
    Create Review object
    """
    dictionary = request.get_json()
    place = storage.get(Place, place_id)
    if place is None:
        abort(404)
    if dictionary is None:
        abort(400, "Not a JSON")
    if "user_id" not in dictionary:
        abort(400, "Missing user_id")
    if storage.get(User, dictionary["user_id"]) is None:
        abort(404)
    if "text" not in dictionary:
        abort(400, "Missing text")
    dictionary["place_id"] = place_id
    review = Review(**dictionary)
    review.save()
    return make_response(jsonify(review.to_dict()), 201)


@app_views.route("/reviews/<review_id>", methods=["PUT"], strict_slashes=False)
def modify_review(review_id):
    """
    Modify Review object
    """
    review = storage.get(Review, review_id)
    dictionary = request.get_json()
    if review is None:
        abort(404)
    if dictionary is None:
        abort(400, "Not a JSON")
    ignored_key = ["id", "user_id", "place_id", "created_at", "updated_at"]
    for key, value in dictionary.items():
        if key not in ignored_key:
            setattr(review, key, value)
    review.save()
    return make_response(jsonify(review.to_dict()), 200)
