#!/usr/bin/python3
"""
This code snippet is setting up a Flask Blueprint named
`app_views` with a URL prefix of `/api/v1`.
Blueprints in Flask are used to organize related
views, templates, and static files.
"""
from flask import Blueprint

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')

from api.v1.views.index import *
from api.v1.views.states import *
from api.v1.views.cities import *
from api.v1.views.amenities import *
