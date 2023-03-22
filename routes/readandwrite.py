from . import *

blueprintReadandWrite = Blueprint('readandwrite', __name__)


@blueprintReadandWrite.route('/readandwrite/fillblank')
def render_fillblank():
    return render_template('admin/pages/readandwrite/fillblank.html')



@blueprintReadandWrite.route('/readandwrite/shortanswer')
def render_shortanswer():
    return render_template('admin/pages/readandwrite/short_answer.html')




@blueprintReadandWrite.route('/readandwrite/photo')
def render_photo():
    return render_template('admin/pages/readandwrite/photo.html')