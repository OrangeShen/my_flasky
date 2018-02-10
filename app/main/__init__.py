from flask import Blueprint


main = Blueprint('main', __name__)
# 'main' indicates the name of the Blueprint
# __name__ indicates the package or module that contains the blueprint

from . import views, errors
from ..models import Permission
# Import at the end of this file to avoid 'import loop'


@main.app_context_processor
def inject_permissions():
    return dict(Permission=Permission)
