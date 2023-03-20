from . import *

blueprintReading = Blueprint('reading', __name__)


@blueprintReading.route('/reading/selectword')
def render_selectword():
    return render_template('admin/pages/reading/select.html')





@blueprintReading.route('/reading/matching')
def render_matching():
    return render_template('admin/pages/reading/matching.html')




@blueprintReading.route('/reading/reading')
def render_reading():
    return render_template('admin/pages/reading/reading.html')