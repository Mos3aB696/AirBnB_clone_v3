from flask import Blueprint
from .index import app_views

app_views = Blueprint('app_views', __name__, url_prefix='/api/v1')
