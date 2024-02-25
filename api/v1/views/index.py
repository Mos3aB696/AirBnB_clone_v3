#!/usr/bin/python3
"""
  This function returns a JSON response with the status "OK" when
  the '/status' endpoint is accessed.
  :return: The status endpoint is returning a JSON response
  with the status "OK".
"""
from flask import jsonify
from api.v1.views import app_views
from models.engine.file_storage import FileStorage


@app_views.route('/status', methods=['GET'])
def status():
    """Return status"""
    return jsonify({"status": "OK"})


@app_views.route('/stats', methods=['GET'])
def get_stats():
    """Return the count of all objects"""
    classes = {"Amenity": "amenities", "City": "cities", "Place": "places",
               "Review": "reviews", "State": "states", "User": "users"}
    stats = {}
    storage = FileStorage()
    for key, value in classes.items():
        stats[value] = storage.count(key)
    return jsonify(stats)
