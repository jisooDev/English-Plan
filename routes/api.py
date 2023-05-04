from . import *
import json
import base64
import random
import traceback
from flask import session
from datetime import datetime
from pytz import timezone
blueprint = Blueprint('api', __name__)



"""
    ประเภทของแบบทดสอบ
    1. การอ่าน => reading => ข้อสอบ Reading  => Read And Select
    2. การเขียน => writing => เขียนตามคำบอก => Listen And Type
    3. เติมคำในช่องว่าง => fillblank => เติมคำใน TEXT  => Reading Section
    4. เลือกคำที่ถูก => choose_word => เลือกคำที่ถูกต้อง => Read And Select
    5. เขียนบรรยายรูป => write_caption => อธิบายรูป (เขียน) => Write About The Photo
    6. พูดบรรยายรูป => speak_subtitle => อธิบายรูป (พูด) => Speak About The Photo
    7. อ่านตามตัวอักษร => read_alphabetically => อ่านตามตัวอักษร => Read Aloud
    8. เขียนตามจำนวนคำ => write_by_number_of_words => ???  => 
"""


def check_user_package():
    try:
        user_id = session.get('user_id')
        if not user_id:
            return False
        else:
            connection = query.get_connection()
            cursor = connection.cursor()
            today = datetime.now(tz=timezone('Asia/Bangkok')).date()
            sql_str = '''SELECT record_id FROM user_packages WHERE user_id = "%s" AND start_date <= "%s" AND end_date >= "%s"'''%(user_id, today, today)

            cursor.execute(sql_str)
            response = cursor.fetchone()

            cursor.close()
            connection.close()
            if response:
                return True
            else:
                return False
        
    except Exception as e:
        traceback.print_exc()
        return  False
  

@blueprint.route('/package/check', methods=['GET'])
def api_check_package():
    try:
        package = check_user_package()
        return  Response(response=json.dumps({'success': True, 'have_package': package, 'is_login': True if session.get('user_id') else False}), mimetype='application/json', status=200)
    
    except Exception as e:
        traceback.print_exc()
        return  Response(response=json.dumps({'success': False}), mimetype='application/json', status=400)

def sort_practice(data):
    for i in range(1, len(data)):
        current_practice_type = data[i]['practice_type']
        previous_practice_type = data[i-1]['practice_type']
        if current_practice_type == previous_practice_type:
            j = random.randint(0, i-1)
            data[i], data[j] = data[j], data[i]
    
    return data

@blueprint.route('/exam/list', methods=['POST'])
def api_get_practice_list():
    try:
        res = request.json
        package = check_user_package()
        is_demo = 0 
        if not package:
            is_demo = 1
            res['tasks'] = 'all'
            res['difficulty'] = 'medium'
        limit = 16
        _filter = ''''''
        practice_total = 0
        connection = query.get_connection()
        cursor = connection.cursor()

        if res['tasks'] == 'all':

            if res['difficulty'] != 'all':
                if len(_filter) == 0:
                    _filter += ' WHERE '
                else:
                    _filter += ' AND '
                _filter += ' difficulty = "%s"'%res['difficulty']
                
            sql_str = f'''SELECT practice_id, practice_type, difficulty, number_of_questions  FROM exam_config {_filter} ORDER BY RAND() LIMIT {limit}'''
            
            cursor.execute(sql_str)
            response = cursor.fetchall()
            if len(response) > 0:
                if res['tasks'] == 'all':
                    random.shuffle(response)
                    for item in response:
                        if item['practice_type'] == 'reading':
                            detail, id = get_practice_reading(cursor, True, item['difficulty'], None, None, is_demo)
                            item['number_of_questions'] = len(detail)
                            item['exam_id'] = id
                        if item['practice_type'] == 'interactive_conversation': 
                            detail, id = get_practice_interactive_conversation(cursor, True, item['difficulty'], None, None, is_demo)
                            item['number_of_questions'] = len(detail)
                            item['exam_id'] = id
                    if limit > len(response):
                        response = fullfill_practice(response, limit)
                    for item in response: 
                        practice_total = practice_total + item['number_of_questions']
                    response = sort_practice(response)
                    response = sort_practice(response)
        else:
            difficulty = res['difficulty'] if res['difficulty'] != 'all' else False
            if res['tasks'] == 'reading':
                response, practice_total = get_practice_reading(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'matching':
                response, practice_total = get_practice_matching(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'reading_select_real_eng_word':
                response, practice_total = get_practice_reading_select_real_eng_word(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'fill_in_blank':
                response, practice_total = get_practice_fill_in_blank(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'short_answer':
                response, practice_total = get_practice_short_answer(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'describe_a_photo':
                response, practice_total = get_practice_describe_a_photo(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'write_down_what_you_hear':
                response, practice_total = get_practice_write_down_what_you_hear(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'listen_select_real_eng_word':
                response, practice_total = get_practice_listen_select_real_eng_word(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'interactive_conversation':
                response, practice_total = get_practice_interactive_conversation(cursor, False, difficulty, False, limit, is_demo)

            if res['tasks'] == 'read_aloud':
                response, practice_total = get_practice_read_aloud(cursor, False, difficulty, False, limit, is_demo)

        cursor.close()
        connection.close()
            
        return  Response(response=json.dumps({'success': True if len(response) else False, 'total': practice_total, 'data': response}), mimetype='application/json', status=200)
    
    except Exception as e:
        traceback.print_exc()
        return  Response(response=json.dumps({'success': False}), mimetype='application/json', status=400)



@blueprint.route('/exam/detail', methods=['GET'])
def api_get_practice_detail():
    try:
        package = check_user_package()
        is_demo = 0 
        if not package:
            is_demo = 1
        connection = query.get_connection()
        cursor = connection.cursor()
        practiceId = request.args.get('practice_id')
        
        examId = request.args.get('exam_id')

        if examId == 'undefined':
            examId = False
        
        sql_str = '''SELECT practice_id, practice_type, practice_name, timer, limited_time, difficulty, number_of_questions FROM exam_config WHERE practice_id  = %s'''%practiceId

        cursor.execute(sql_str)
        practice = cursor.fetchone()
        result = {
            'practice_id': practice['practice_id'],
            'practice_type': practice['practice_type'],
            'practice_name': practice['practice_name'],
            'number_of_questions': practice['number_of_questions'],
            'limited_time': True if practice.get('limited_time') else False,
            'timer': practice['timer'],
            'difficulty': practice['difficulty'],
        }
        if practice['practice_type'] == "reading":
            result['data'], _ = get_practice_reading(cursor, True, practice['difficulty'], examId, 1, is_demo)
            
        if practice['practice_type'] == "matching":
            data, _ = get_practice_matching(cursor, True, practice['difficulty'], examId, 1, is_demo)
            result['data'] = data['data']
            result['options'] = data['option']

        if practice['practice_type'] == "reading_select_real_eng_word":
            result['data'], _ = get_practice_reading_select_real_eng_word(cursor, True, False, examId, 12, is_demo)
           
            
        if practice['practice_type'] == "fill_in_blank":
            data, _ = get_practice_fill_in_blank(cursor, True, False, examId, 1, is_demo)
            result['data'] = data['data']
            result['answer'] = data['answer']

        if practice['practice_type'] == "short_answer":
            data, _ = get_practice_short_answer(cursor, True, False, examId, 1, is_demo)
            result['data'] = data['data']
            result['answer'] = data['answer']

        if practice['practice_type'] == "describe_a_photo":
            data, _ = get_practice_describe_a_photo(cursor, True, False, examId, 1, is_demo)
            result['data'] = data['data']
            result['answer'] = data['answer']

        if practice['practice_type'] == "write_down_what_you_hear":
            data, _ = get_practice_write_down_what_you_hear(cursor, True, False, examId, 1, is_demo)
            result['data'] = data['data']
            result['answer'] = data['answer']
            

        if practice['practice_type'] == "listen_select_real_eng_word":
            result['data'], _ = get_practice_listen_select_real_eng_word(cursor, True, False, examId, 12, is_demo)
            
            
        if practice['practice_type'] == "interactive_conversation":
            result['data'], _ = get_practice_interactive_conversation(cursor, True, False, examId, 1, is_demo)

        if practice['practice_type'] == "read_aloud":
            data, _ = get_practice_read_aloud(cursor, True, False, examId, 1, is_demo)
            result['data'] = data['data']
            result['answer'] = data['answer']
            result['audio'] = data['audio']
       

        return  Response(response=json.dumps({'success': True, 'data': result}), mimetype='application/json', status=200)

    except Exception as e:
        traceback.print_exc()
        return  Response(response=json.dumps({'success': False, 'data': None, 'message': str(e)}), mimetype='application/json', status=400)
    finally:
        cursor.close()
        connection.close()


def fullfill_practice(data, limit):
    result = []
    for i in range(limit):
        random_index = random.randint(0, len(data) - 1)
        result.append(data[random_index])
    return result

        
def get_practice_reading(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, json_data FROM reading_reading WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, json_data FROM reading_reading WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return json.loads(data['json_data']), data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, aa.number_of_questions
                    FROM reading_reading aa
                    LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "reading" 
                    {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        total = 0
        for item in data:
            if total >= limit:
                del item
            else:
                total = total + int(item['number_of_questions'])

        if limit > total:
            data = fullfill_practice(data, int(limit / data[0]['number_of_questions']))
            total = 0
            for item in data:
                total = total + int(item['number_of_questions'])
        return data, total
            

def get_practice_matching(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, json_data, json_option FROM reading_matching WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, json_data, json_option FROM reading_matching WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': json.loads(data['json_data']), 'option': json.loads(data['json_option'])}, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM reading_matching aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "matching" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_reading_select_real_eng_word(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, value, answer_atob AS answer FROM reading_select_words WHERE id = "{id}" LIMIT {limit}'''
        else:
            sql_str = f'''SELECT id, value, answer_atob AS answer FROM reading_select_words WHERE is_demo = {is_demo} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        return data, None
    
    else:
        _filter = ' WHERE bb.practice_type = "reading_select_real_eng_word" '
        if difficulty:
            _filter = _filter + f''' AND bb.difficulty = "{difficulty}"'''
        
        sql_str = f'''SELECT bb.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions 
                FROM exam_config bb {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_fill_in_blank(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, data, answer FROM readandwrite_fill_blank WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, data, answer FROM readandwrite_fill_blank WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': data['data'], 'answer': json.loads(data['answer'])}, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM readandwrite_fill_blank aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "fill_in_blank" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_short_answer(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM readandwrite_short_answer WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM readandwrite_short_answer WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': data['data'], 'answer': data['answer']}, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM readandwrite_short_answer aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "short_answer" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_describe_a_photo(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM readandwrite_describe_photo WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM readandwrite_describe_photo WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': data['data'], 'answer': data['answer']}, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM readandwrite_describe_photo aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "describe_a_photo" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_write_down_what_you_hear(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM listening_write_down WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, data, answer_atob AS answer FROM listening_write_down WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': data['data'], 'answer': data['answer']}, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f'''WHERE aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM listening_write_down aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "write_down_what_you_hear" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_listen_select_real_eng_word(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, name, data AS value, answer_atob AS answer FROM listening_select_words WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, name, data AS value, answer_atob AS answer FROM listening_select_words WHERE is_demo = {is_demo} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        return data, len(data)
    
    else:
    
        _filter = ' WHERE bb.practice_type = "listen_select_real_eng_word" '
        if difficulty:
            _filter = _filter + f''' AND bb.difficulty = "{difficulty}"'''
        
        sql_str = f'''SELECT bb.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions 
                FROM exam_config bb {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)

def get_practice_interactive_conversation(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, json_data, audio FROM listening_interactive_conversation WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, json_data, audio FROM listening_interactive_conversation WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        json_data = json.loads(data['json_data'])
        for item in json_data:
            if not item.get('audio'):
                item['audio'] = data['audio']
        return json_data, data['id']
    
    else:
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, aa.number_of_questions
                    FROM listening_interactive_conversation aa
                    LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "interactive_conversation" 
                    {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        total = 0
        for item in data:
            if total >= limit:
                del item
            else:
                total = total + int(item['number_of_questions'])
        if limit > total:
            data = fullfill_practice(data, int(limit / data[0]['number_of_questions']))
            total = 0
            for item in data:
                total = total + int(item['number_of_questions'])
        return data, total
    

def get_practice_read_aloud(cursor, get_detail, difficulty, id, limit, is_demo):
    if get_detail:
        if id:
            sql_str = f'''SELECT id, data, answer_atob AS answer, audio FROM talking_read_aloud WHERE id = "{id}"'''
        else:
            sql_str = f'''SELECT id, data, answer_atob AS answer, audio FROM talking_read_aloud WHERE difficulty = "{difficulty}" AND is_demo = {is_demo} ORDER BY RAND() LIMIT 1'''
        cursor.execute(sql_str)
        data = cursor.fetchone()
        return {'data': data['data'], 'answer': data['answer'], 'audio': data['audio']}, data['id']
    
    else:
    
        _filter = f' WHERE aa.is_demo = {is_demo}'
        if difficulty:
            _filter = f''' AND aa.difficulty = "{difficulty}"'''
        sql_str = f'''SELECT aa.id AS exam_id, aa.difficulty, bb.practice_id, bb.practice_type, bb.number_of_questions
                FROM talking_read_aloud aa
                LEFT JOIN exam_config bb ON aa.difficulty = bb.difficulty AND bb.practice_type = "read_aloud" 
                {_filter} ORDER BY RAND() LIMIT {limit}'''
        cursor.execute(sql_str)
        data = cursor.fetchall()
        if limit > len(data):
            data = fullfill_practice(data, limit)
        
        return data, len(data)


btoa = lambda x:base64.b64decode(x)
atob = lambda x:base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')
