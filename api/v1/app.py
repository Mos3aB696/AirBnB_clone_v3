#!/usr/bin/python3
"""
  This Python script sets up a Flask web application with API
  routes and a database connection that
  closes when the application context is torn down.

  :param exception: The `exception` parameter in the `teardown_appcontext`
  function is a reference to any exception that might have occurred
  during the application context. This parameter allows you to handle
  exceptions or perform cleanup actions before the application context
  is torn down. In your
  code snippet, the `teardown_appcontext`
"""
from flask import Flask
from api.v1.views import app_views
from models import storage
import os

app = Flask(__name__)

app.register_blueprint(app_views)


@app.teardown_appcontext
def teardown_appcontext(exception):
    storage.close()


if __name__ == "__main__":
    host = os.environ.get('HBNB_API_HOST', '0.0.0.0')
    port = int(os.environ.get('HBNB_API_PORT', 5000))
    app.run(host=host, port=port, threaded=True)
