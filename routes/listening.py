from . import *

blueprintListening = Blueprint('listening', __name__)


atob = lambda x:base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')

@blueprintListening.route('/listening/writedown')
def render_writedown():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,answer,data FROM listening_write_down
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
    except Exception as e :
        print(e)

    return render_template('admin/pages/listening/writedown.html' , response=response)

@blueprintListening.route('/listening/writedown/delete/<_id>')
def del_writedown(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try : 
        sql_str = '''
            DELETE FROM listening_write_down 
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

        storage_delete.delete("lintening/writedown/%s"%_id)
    except Exception as e :
        print(e)

    return redirect('/admin/listening/writedown')

@blueprintListening.route('/listening/writedown/create', methods=[ 'GET' , 'POST'])
def create_writedown():

    if request.method == 'POST':
        try :
            difficulty = request.form['difficulty']
            files = request.files.getlist('data[]')
            answers = request.form.getlist('answer[]')
            
            connection = query.get_connection()
            cursor = connection.cursor()
            sql_data = []
            for file , answer in zip(files , answers) :
                file_data = file.read()
                _uuid = uuid.uuid4().hex
                storage.child('lintening/writedown/%s'%_uuid).put(file_data)
                _url = storage.child('lintening/writedown/%s'%_uuid).get_url(None)
                
                sql_data.append((_uuid , difficulty , _url ,answer , atob(answer) ))


            sql_str = '''
                INSERT INTO listening_write_down
                (id , difficulty , data ,  answer , answer_atob)
                VALUES
                (%s ,%s ,%s ,%s ,%s)
            '''
            cursor.executemany(sql_str, sql_data)
            connection.commit()
        except Exception as e :
            print(e)

        return redirect('/admin/listening/writedown')




    return render_template('admin/pages/listening/writedown_create.html')




@blueprintListening.route('/listening/selectword')
def render_selectword():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,name,answer,data FROM listening_select_words
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
    except Exception as e :
        print(e)

    return render_template('admin/pages/listening/select.html' , response=response)

@blueprintListening.route('/listening/selectword/create', methods=[ 'GET' , 'POST'])
def create_selectword():

    if request.method == 'POST':

        try :

            difficulty = request.form['difficulty']
        
            files = request.files.getlist('data[]')
            answers = request.form.getlist('answer[]')
            values = request.form.getlist('value[]')
            
            connection = query.get_connection()
            cursor = connection.cursor()
            sql_data = []
            for file , answer , value in zip(files , answers , values) :
                file_data = file.read()
                _uuid = uuid.uuid4().hex
                storage.child('lintening/selectword/%s'%_uuid).put(file_data)
                _url = storage.child('lintening/selectword/%s'%_uuid).get_url(None)
                
                sql_data.append((_uuid , value , difficulty , _url , answer , atob(value)))


            sql_str = '''
                INSERT INTO listening_select_words
                (id , answer, difficulty , data ,  name , answer_atob )
                VALUES
                (%s ,%s ,%s ,%s , %s , %s)
            '''
            cursor.executemany(sql_str, sql_data)
            connection.commit()
        except Exception as e :
            print(e)

        return redirect('/admin/listening/selectword')




    return render_template('admin/pages/listening/select_create.html')

@blueprintListening.route('/listening/selectword/delete/<_id>')
def del_selectword(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            DELETE FROM listening_select_words 
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()
        storage_delete.delete("lintening/selectword/%s"%_id)

    except Exception as e :
        print(e)

    return redirect('/admin/listening/selectword')


@blueprintListening.route('/listening/interactive')
def render_matching():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,json_data,audio FROM listening_interactive_conversation
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/listening/interactive.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintListening.route('/listening/interactive/create' , methods=[ 'GET' , 'POST'])
def render_matching_create():

    if request.method == 'POST':
        try :
            file = request.files['audio']
            json_data = request.form.get('data')
            difficulty = request.form.get('difficulty')

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex


            reformat_json = json.loads(json_data)

            for item in reformat_json :
                item['answer'] = atob(item['answer'])

            file_data = file.read()
            storage.child('lintening/interactive/%s'%_uuid).put(file_data)
            _url = storage.child('lintening/interactive/%s'%_uuid).get_url(None)

            sql_data = (_uuid , difficulty, _url , json.dumps(reformat_json))
            sql_str = '''
                INSERT INTO listening_interactive_conversation
                (id , difficulty, audio, json_data)
                VALUES
                (%s , %s, %s ,%s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/listening/interactive')
    else :
        return render_template('admin/pages/listening/interactive_create.html')

@blueprintListening.route('/listening/interactive/delete/<_id>')
def del_matching(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            DELETE FROM listening_interactive_conversation 
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()
        storage_delete.delete("lintening/interactive/%s"%_id)

    except Exception as e :
        print(e)

    return redirect('/admin/listening/interactive')