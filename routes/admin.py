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
            SELECT us.id ,us.email , pk.name, up.record_id , up.start_date , up.end_date
            FROM user_packages up
            LEFT JOIN users us ON us.id = up.user_id 
            LEFT JOIN packages pk ON up.package_id = pk.id 
            WHERE up.active = "1" and us.role != "admin"
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()


        sql_str_user = '''
            SELECT email , id 
            FROM users
            WHERE active = "1" and role != "admin"
        '''

        cursor.execute(sql_str_user)
        all_email = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/super/super.html' , response=response , all_email=json.dumps(all_email))


@blueprintAdmin.route('/super/approve'  , methods=[ 'POST' , 'GET'])
def admin_super_approve():
    try :
        payload = request.json
        query.handle_checkout_session(payload['user_id'] , payload['package_id'])
    except Exception as e :
        print(e)

    return redirect('/admin/super')

@blueprintAdmin.route('/super/unapprove/<int:user_id>/<int:record_id>')
def admin_super_unapprove(user_id, record_id):
    try:
        connection = query.get_connection()
        cursor = connection.cursor()

        sql_str = '''
        UPDATE user_packages
        SET active = 0 
        WHERE record_id = %s and user_id = %s
        '''%(record_id, user_id)

        cursor.execute(sql_str)
        connection.commit()

    except Exception as e:
        print(e)
        return "An error occurred while processing your request", 500

    return redirect('/admin/super')
