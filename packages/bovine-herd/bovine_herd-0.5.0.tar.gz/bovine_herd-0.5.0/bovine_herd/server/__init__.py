from quart import Blueprint

from .activitypub import activitypub
from .wellknown import wellknown

default_configuration = Blueprint("default_configuration", __name__)
default_configuration.register_blueprint(wellknown)
default_configuration.register_blueprint(activitypub)
