from . import *

blueprint = Blueprint('admin', __name__)

@blueprint.route('/')
def empty_path():
    return 'hello Admin'