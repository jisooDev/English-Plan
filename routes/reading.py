from . import *

blueprintReading = Blueprint('reading', __name__)


@blueprintReading.route('/reading/selectword')
def render_selectword():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,value,answer FROM reading_select_words
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
    except Exception as e :
        print(e)
    return render_template('admin/pages/reading/select.html' , response=response)


@blueprintReading.route('/reading/selectword/create', methods=[ 'GET' , 'POST'])
def create_selectword():

    if request.method == 'POST':

        try :
            difficulty = request.form['difficulty']
            answers = request.form.getlist('answer[]')
            values = request.form.getlist('value[]')
            
            connection = query.get_connection()
            cursor = connection.cursor()
            sql_data = []
            for  answer , value in zip( answers , values) :
                _uuid = uuid.uuid4().hex
                
                sql_data.append((_uuid , value , difficulty , answer , atob(value)))


            sql_str = '''
                INSERT INTO reading_select_words
                (id , answer, difficulty , value , answer_atob )
                VALUES
                (%s ,%s ,%s ,%s , %s)
            '''
            cursor.executemany(sql_str, sql_data)
            connection.commit()
        except Exception as e :
            print(e)

        return redirect('/admin/reading/selectword')


    return render_template('admin/pages/reading/select_create.html')

@blueprintReading.route('/reading/selectword/delete/<_id>')
def del_selectword(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try : 
        sql_str = '''
            DELETE FROM reading_select_words 
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/reading/selectword')


@blueprintReading.route('/reading/reading')
def render_reading():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,json_data FROM reading_reading
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/reading/reading.html' , response=response , json=json , atob=atob , btoa=btoa)


@blueprintReading.route('/reading/reading/create' , methods=[ 'GET' , 'POST'])
def render_reading_create():

    if request.method == 'POST':
        try :
            json_data = request.form.get('data')
            difficulty = request.form.get('difficulty')

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex

            reformat_json = json.loads(json_data)

            for item in reformat_json :
                item['answer'] = atob(item['answer'])

            sql_data = (_uuid , difficulty , json.dumps(reformat_json))
            sql_str = '''
                INSERT INTO reading_reading
                (id , difficulty, json_data)
                VALUES
                (%s , %s, %s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/reading/reading')
    else :
        return render_template('admin/pages/reading/reading_create.html')


@blueprintReading.route('/reading/reading/delete/<_id>')
def del_reading(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            DELETE FROM reading_reading 
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/reading/reading')



@blueprintReading.route('/reading/matching')
def render_matching():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT id,difficulty,json_data,json_option FROM reading_matching
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/reading/matching.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintReading.route('/reading/matching/create' , methods=[ 'GET' , 'POST'])
def render_matching_create():

    if request.method == 'POST':
        try :
            json_data = request.form.get('json_data')
            json_options = request.form.get('json_option')
            difficulty = request.form.get('difficulty')

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex

            reformat_json = json.loads(json_data)
            for item in reformat_json :
                item['answer'] = atob(item['answer'])

            reformat_option = json.loads(json_options)
            for item in reformat_option :
                item['answer'] = atob(item['answer'])

            sql_data = (_uuid , difficulty , json.dumps(reformat_json) , json.dumps(reformat_option))
            sql_str = '''
                INSERT INTO reading_matching
                (id , difficulty, json_data , json_option)
                VALUES
                (%s , %s, %s, %s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

    return render_template('admin/pages/reading/matching_create.html')


@blueprintReading.route('/reading/matching/delete/<_id>')
def del_matching(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            DELETE FROM reading_matching
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/reading/matching')