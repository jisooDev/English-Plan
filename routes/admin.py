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


@blueprintAdmin.route('/super')
def admin_super():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,name,role FROM users
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/super/super.html' , response=response)

