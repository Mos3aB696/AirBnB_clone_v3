#!/usr/bin/python3
"""Creating flask app."""

from api.v1.views import app_views
from flask import Flask, jsonify
from models import storage
from os import getenv
from flask_cors import CORS
app = Flask(__name__)
app.register_blueprint(app_views)


cors = CORS(app, resources={r"/api/*": {"origins": "0.0.0.0"}})


@app.teardown_appcontext
def teardown_appcontext(self):
    """Close the storage."""
    storage.close()


@app.errorhandler(404)
def error_handler(error):
    """Handle for 404 errors."""
    return jsonify({"error": "Not found"}), 404


if __name__ == "__main__":
    host = getenv("HBNB_API_HOST", "0.0.0.0")
    port = getenv("HBNB_API_PORT", "5000")

    app.run(host=host, port=port, threaded=True)
