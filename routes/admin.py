from . import *

blueprint = Blueprint('admin', __name__)

@blueprint.route('/')
def empty_path():
    return render_template('admin/pages/index.html')