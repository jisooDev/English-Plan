from . import *

blueprintTalking = Blueprint('talking', __name__)


@blueprintTalking.route('/talking/interactive')
def render_interactive():
    return render_template('admin/pages/talking/interactive.html')
