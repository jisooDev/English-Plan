from . import *

blueprintAdmin = Blueprint('admin', __name__)

@blueprintAdmin.route('/')
def empty_path():
    if  session["role"] == "admin":
        return redirect('dashboard')
    else:
        return render_template('main.html')

@blueprintAdmin.route('/dashboard')
def dashboard():
    return render_template('admin/pages/index.html')

