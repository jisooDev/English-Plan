from crypt import methods
from . import *

blueprintListening = Blueprint('listening', __name__)


@blueprintListening.route('/listening/writedown')
def render_selectword():
    return render_template('admin/pages/listening/writedown.html')

@blueprintListening.route('/listening/writedown/create', methods=['POST'])
def create_selectword():
    with open('test_audio.mp3', 'rb') as file:

        file_content = file.read()
        storage.child('audio/' + 'test').put(file_content)

    return '200'



@blueprintListening.route('/listening/interactive')
def render_matching():
    return render_template('admin/pages/listening/interactive.html')




@blueprintListening.route('/listening/selectword')
def render_reading():
    return render_template('admin/pages/listening/select.html')