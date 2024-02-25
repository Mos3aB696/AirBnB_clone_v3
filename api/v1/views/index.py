#!/usr/bin/python3
"""
  This function returns a JSON response with the status "OK" when
  the '/status' endpoint is accessed.
  :return: The status endpoint is returning a JSON response
  with the status "OK".
"""
from flask import jsonify
from api.v1.views import app_views


@app_views.route('/status', methods=['GET'])
def status():
    """Return status"""
    return jsonify({"status": "OK"})
