from . import *

blueprintReadandWrite = Blueprint('readandwrite', __name__)


@blueprintReadandWrite.route('/readandwrite/shortanswer')
def render_shortanswer():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT * FROM readandwrite_short_answer WHERE active = 1
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/readandwrite/short_answer.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintReadandWrite.route('/readandwrite/shortanswer/create' , methods=[ 'GET' , 'POST'])
def render_shortanswer_create():

    if request.method == 'POST':
        try :
            data = request.form.get('data')
            answer = request.form.get('answer')
            difficulty = request.form.get('difficulty')

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex


            sql_data = (_uuid , difficulty , data , answer)
            sql_str = '''
                INSERT INTO readandwrite_short_answer
                (id , difficulty, data , answer)
                VALUES
                (%s , %s, %s ,%s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/readandwrite/shortanswer')
    else :
        return render_template('admin/pages/readandwrite/short_answer_create.html')

@blueprintReadandWrite.route('/readandwrite/shortanswer/delete/<_id>')
def del_read(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            UPDATE readandwrite_short_answer SET active = 0
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/readandwrite/shortanswer')


@blueprintReadandWrite.route('/readandwrite/describephoto')
def render_describephoto():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT * FROM readandwrite_describe_photo WHERE active = 1
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/readandwrite/describe_photo.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintReadandWrite.route('/readandwrite/describephoto/create' , methods=[ 'GET' , 'POST'])
def render_describephoto_create():

    if request.method == 'POST':
        try :
            data = request.files['data']
            answer = request.form.get('answer')
            difficulty = request.form.get('difficulty')

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex

            file_data = data.read()
            storage.child('readandwrite/describephoto/%s'%_uuid).put(file_data)
            _url = storage.child('readandwrite/describephoto/%s'%_uuid).get_url(None)

            sql_data = (_uuid , difficulty , _url , answer,atob(answer))
            sql_str = '''
                INSERT INTO readandwrite_describe_photo
                (id , difficulty, data , answer, answer_atob)
                VALUES
                (%s , %s, %s , %s , %s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/readandwrite/describephoto')
    else :
        return render_template('admin/pages/readandwrite/describe_photo_create.html')

@blueprintReadandWrite.route('/readandwrite/describephoto/delete/<_id>')
def del_describephoto(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            UPDATE readandwrite_describe_photo SET active = 0
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/readandwrite/describephoto')

@blueprintReadandWrite.route('/readandwrite/fillblank')
def render_fillblank():
    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            SELECT * FROM readandwrite_fill_blank WHERE active = 1
        '''
        cursor.execute(sql_str)
        response = cursor.fetchall()
        
    except Exception as e :
        print(e)

    return render_template('admin/pages/readandwrite/fillblank.html' , response=response , json=json , atob=atob , btoa=btoa)

@blueprintReadandWrite.route('/readandwrite/fillblank/create' , methods=[ 'GET' , 'POST'])
def render_fillblank_create():

    if request.method == 'POST':
        try :
            dataJson = request.json

            data = dataJson['data']
            data_atob = dataJson["data_atob"]
            answer = dataJson['answer']
            difficulty = dataJson['difficulty']

            new_answer = []
            for x in answer:
                new_answer.append({
                    "value": atob(x["value"]),
                    "show": x["show"]
                })

            connection = query.get_connection()
            cursor = connection.cursor()
            _uuid = uuid.uuid4().hex

            find_word = dataJson['find_word']

            _card = []
            _index = 0
            for vocab in find_word :
                _text = ''

                for _ in vocab :
                    _text += '{{%s}}'%_index
                    _index += 1

                _card.append(_text)

            _result = data%tuple(_card)

            sql_data = (_uuid , difficulty , _result , data_atob , json.dumps(new_answer))
            sql_str = '''
                INSERT INTO readandwrite_fill_blank
                (id , difficulty, data , data_atob ,answer)
                VALUES
                (%s , %s, %s ,%s , %s)
            '''
            cursor.execute(sql_str, sql_data)
            connection.commit()

        except Exception as e :
            print(e)

        return redirect('/admin/readandwrite/fillblank')
    else :
        return render_template('admin/pages/readandwrite/fillblank_create.html')

@blueprintReadandWrite.route('/readandwrite/fillblank/delete/<_id>')
def del_fillblank(_id):    

    connection = query.get_connection()
    cursor = connection.cursor()

    try :
        sql_str = '''
            UPDATE readandwrite_fill_blank SET active = 0
            WHERE id = "%s";
        '''%_id
        cursor.execute(sql_str)
        connection.commit()

    except Exception as e :
        print(e)

    return redirect('/admin/readandwrite/fillblank')

