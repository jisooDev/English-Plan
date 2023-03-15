from . import *
import json
import base64
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

@blueprint.route('/practice/list', methods=['POST'])
def api_get_parctice_list():
    res = request.json
    print(res)
    return  Response(response=json.dumps({'success': True, 'data': [{
        'practice_id': 1,
        'practice_type': 'reading'
    },{
        'practice_id': 2,
        'practice_type': 'writing'
    },{
        'practice_id': 3,
        'practice_type': 'fillblank'
    },{
        'practice_id': 4,
        'practice_type': 'choose_word'
    },{
        'practice_id': 5,
        'practice_type': 'write_caption'
    },{
        'practice_id': 6,
        'practice_type': 'speak_subtitle'
    },{
        'practice_id': 7,
        'practice_type': 'read_alphabetically'
    },{
        'practice_id': 8,
        'practice_type': 'write_by_number_of_words'
    }]}), mimetype='application/json', status=200)


btoa = lambda x:base64.b64decode(x)
atob = lambda x:base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')

@blueprint.route('/practice/detail', methods=['GET'])
def api_get_parctice_detail():
    try:
        practiceId = request.args.get('practice_id')
        practiceType = request.args.get('practice_type')
        print(practiceId)
        return  Response(response=json.dumps({'success': True, 'data': practice_1}), mimetype='application/json', status=200)

    except Exception as e:
        print(e)
        return  Response(response=json.dumps({'success': False, 'data': None, 'message': str(e)}), mimetype='application/json', status=400)
    




practice_1 = {
    'practice_id': 1,
    'practice_type': 'reading',
    'timer': 300,
    'difficulty': 'medium',
    'story': '''European history is a fascinating and complex subject that covers a vast time period, from ancient Greece and Rome to the present day. It is a history of conquest, expansion, and colonization, as well as religious and political conflicts that have shaped the continent's social, cultural, and economic development. One of the defining features of European history is the influence of the Roman Empire, which left a lasting legacy in architecture, law, language, and culture. Another significant event was the Protestant Reformation, which challenged the authority of the Catholic Church and led to centuries of religious conflict. The Age of Exploration and the Industrial Revolution was also pivotal moments in European history, transforming the continent's economy, technology, and global influence. Finally, the two World Wars, and the subsequent creation of the European Union, marked a new era of cooperation and integration but also highlighted the enduring challenges of nationalism, racism, and inequality.''',
    'quiz': [{
        'id': 1,
        'question': 'What were some of the defining features of European history?',
        'answer': atob('1c'),
        'choice': [{
            'id': '1a',
            'value': 'Its influence of the British Empire'
        },{
            'id': '1b',
            'value': 'Its impact on Asian countries'
        },{
            'id': '1c',
            'value': 'The legacy of the Roman Empire'
        },{
            'id': '1d',
            'value': 'Its contribution to African development'
        }]
    },{
        'id': 2,
        'question': 'Which of the following titles best describes the passage?',
        'answer': atob('2c'),
        'choice': [{
            'id': '2a',
            'value': 'The Rise and Fall of the Roman Empire'
        },{
            'id': '2b',
            'value': 'A Brief History of European Architecture'
        },{
            'id': '2c',
            'value': 'European History: From Ancient Times to the Present Day'
        },{
            'id': '2d',
            'value': 'The Industrial Revolution and Its Impact on Europe'
        }]
    },{
        'id': 3,
        'question': 'What could be a synonym for "conquest" in the passage?',
        'answer': atob('3d'),
        'choice': [{
            'id': '3a',
            'value': 'Battle'
        },{
            'id': '3b',
            'value': 'Victory'
        },{
            'id': '3c',
            'value': 'Occupation'
        },{
            'id': '3d',
            'value': 'Expansion'
        }]
    },{
        'id': 4,
        'question': 'What could be a synonym for "pivotal" in the passage?',
        'answer': atob('4a'),
        'choice': [{
            'id': '4a',
            'value': 'Critical'
        },{
            'id': '4b',
            'value': 'Unimportant'
        },{
            'id': '4c',
            'value': 'Negligible'
        },{
            'id': '4d',
            'value': 'Irrelevant'
        }]
    }]
}