#!/usr/bin/python3
"""
  This code snippet is setting up a Flask Blueprint named `app_views`
  with a URL prefix of `/api/v1`.
  It then imports views from the `index.py` file located in the
  `api/v1/views` directory.
"""
from flask import Blueprint
app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
