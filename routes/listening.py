from . import *

blueprintListening = Blueprint('listening', __name__)


@blueprintListening.route('/listening/writedown')
def render_selectword():
    return render_template('admin/pages/listening/writedown.html')



@blueprintListening.route('/listening/interactive')
def render_matching():
    return render_template('admin/pages/listening/interactive.html')




@blueprintListening.route('/listening/selectword')
def render_reading():
    return render_template('admin/pages/listening/select.html')