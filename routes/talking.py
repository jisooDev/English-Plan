from . import *

blueprintTalking = Blueprint('talking', __name__)


@blueprintTalking.route('/talking/read')
def render_matching():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT * FROM talking_read_aloud WHERE active = 1
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/talking/read.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintTalking.route('/talking/read/create' , methods=[ 'GET' , 'POST'])
def render_read_create():

    if request.method == 'POST':
        try :
            data = request.form.get('data')
            answer = request.form.get('answer')
            difficulty = request.form.get('difficulty')
            file = request.files['audio']

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex

            file_data = file.read()
            storage.child('talking/read_aloud/%s'%_uuid).put(file_data)
            _url = storage.child('talking/read_aloud/%s'%_uuid).get_url(None)

            sql_data = (_uuid , difficulty , data , answer , _url)
            sql_str = '''
                INSERT INTO talking_read_aloud
                (id , difficulty, data , answer , audio)
                VALUES
                (%s , %s, %s ,%s ,%s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/talking/read')
    else :
        return render_template('admin/pages/talking/read_create.html')

@blueprintTalking.route('/talking/read/delete/<_id>')
def del_read(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            UPDATE talking_read_aloud SET active = 0
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/talking/read')
