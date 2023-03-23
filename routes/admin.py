from . import *

blueprintAdmin = Blueprint('admin', __name__)

@blueprintAdmin.route('/')
def empty_path():
    return redirect('dashboard')

@blueprintAdmin.route('/dashboard')
def dashboard():
    return render_template('admin/pages/index.html')

