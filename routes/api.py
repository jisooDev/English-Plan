from . import *
import json
import base64
import random
import traceback
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

@blueprint.route('/exam/list', methods=['POST'])
def api_get_parctice_list():
    try:
        connection = query.get_connection()
        cursor = connection.cursor()
        res = request.json
        print(res)

        _filter = ''''''

        if res['tasks'] != 'all':
            if len(_filter) == 0:
                _filter += ' WHERE '
            else:
                _filter += ' AND '
            _filter += ' practice_type = "%s"'%res['tasks']

        if res['difficulty'] != 'all':
            if len(_filter) == 0:
                _filter += ' WHERE '
            else:
                _filter += ' AND '
            _filter += ' difficulty = "%s"'%res['difficulty']
            
        sql_str = '''
            SELECT practice_id, practice_type, number_of_questions  FROM exam_config %s ORDER BY RAND() LIMIT 16
        '''%(_filter)
        cursor.execute(sql_str)
        response = cursor.fetchall()

        practice_total = 0
        if len(response) > 0:
            random.shuffle(response)

            practice_total = practice_total + response[0]['number_of_questions']
            
            for i in range(1, len(response)):
                practice_total = practice_total + response[i]['number_of_questions']
                current_practice_type = response[i]['practice_type']
                previous_practice_type = response[i-1]['practice_type']
                if current_practice_type == previous_practice_type:
                    j = random.randint(0, i-1)
                    response[i], response[j] = response[j], response[i]
            
            for i in range(1, len(response)):
                current_practice_type = response[i]['practice_type']
                previous_practice_type = response[i-1]['practice_type']
                if current_practice_type == previous_practice_type:
                    j = random.randint(0, i-1)
                    response[i], response[j] = response[j], response[i]

        return  Response(response=json.dumps({'success': True if len(response) else False, 'total': practice_total, 'data': response}), mimetype='application/json', status=200)
    
    except Exception as e:
        traceback.print_exc()
        print(e)
        return  Response(response=json.dumps({'success': False}), mimetype='application/json', status=400)
    finally:
        cursor.close()
        connection.close()



btoa = lambda x:base64.b64decode(x)
atob = lambda x:base64.b64encode(bytes(x, 'utf-8')).decode('utf-8')

@blueprint.route('/exam/detail', methods=['GET'])
def api_get_parctice_detail():
    try:
        connection = query.get_connection()
        cursor = connection.cursor()
        practiceId = request.args.get('practice_id')
        print(practiceId)
        
        sql_str = '''SELECT practice_id, practice_type, practice_name, timer, limited_time, difficulty, number_of_questions FROM exam_config WHERE practice_id  = %s'''%practiceId

        cursor.execute(sql_str)
        practice = cursor.fetchone()
        print(practice)
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
            sql_str = '''SELECT json_data FROM reading_reading WHERE difficulty = "%s" ORDER BY RAND() LIMIT 1'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchone()
            result['data'] = json.loads(data['json_data'])
            
        if practice['practice_type'] == "matching":
            sql_str = '''SELECT json_data, json_option FROM reading_matching WHERE difficulty = "%s" ORDER BY RAND() LIMIT 1'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchone()
            result['data'] = json.loads(data['json_data'])
            result['options'] = json.loads(data['json_option'])

        if practice['practice_type'] == "reading_select_real_eng_word":
            sql_str = '''SELECT id, value, answer_atob AS answer FROM reading_select_words WHERE difficulty = "%s" ORDER BY RAND() LIMIT 12'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchall()
            result['data'] = data
            
        if practice['practice_type'] == "fill_in_blank":
            result = practice_fill_in_blank

        if practice['practice_type'] == "short_answer":
            result = practice_short_answer

        if practice['practice_type'] == "describe_a_photo":
            result = practice_describe_a_photo

        if practice['practice_type'] == "write_down_what_you_hear":
            sql_str = '''SELECT data, answer_atob FROM listening_write_down WHERE difficulty = "%s" ORDER BY RAND() LIMIT 1'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchone()
            result['data'] = data['data']
            result['answer'] = data['answer_atob']

        if practice['practice_type'] == "listen_select_real_eng_word":
           
            sql_str = '''SELECT id, name, data AS value, answer_atob AS answer FROM listening_select_words WHERE difficulty = "%s" ORDER BY RAND() LIMIT 12'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchall()
            result['data'] = data
            
        if practice['practice_type'] == "interactive_conversation":
            sql_str = '''SELECT json_data, audio FROM listening_interactive_conversation WHERE difficulty = "%s" ORDER BY RAND() LIMIT 1'''%practice['difficulty']
            cursor.execute(sql_str)
            data = cursor.fetchone()
            result['data'] = json.loads(data['json_data'])
            result['audio'] = data['audio']

        if practice['practice_type'] == "read_aloud":
            result = practice_read_aloud
        # result = practice_reading
        # if practiceId == "1":
        #     result = practice_reading

        # if practiceId == "2":
        #     result = practice_matching

        # if practiceId == "3":
        #     result = practice_reading_select_real_eng_word
        
        # if practiceId == "4":
        #     result = practice_fill_in_blank

        # if practiceId == "5":
        #     result = practice_short_answer

        # if practiceId == "6":
        #     result = practice_describe_a_photo

        # if practiceId == "7":
        #     result = practice_write_down_what_you_hear

        # if practiceId == "8":
        #     result = practice_listen_select_real_eng_word

        # if practiceId == "9":
        #     result = practice_interactive_conversation

        # if practiceId == "10":
        #     result = practice_read_aloud

        

        return  Response(response=json.dumps({'success': True, 'data': result}), mimetype='application/json', status=200)

    except Exception as e:
        traceback.print_exc()
        return  Response(response=json.dumps({'success': True, 'data': practice_short_answer}), mimetype='application/json', status=200)
        return  Response(response=json.dumps({'success': False, 'data': None, 'message': str(e)}), mimetype='application/json', status=400)
    finally:
        cursor.close()
        connection.close()
    
# practice_reading
# practice_matching
# practice_reading_select_real_eng_word
# practice_fill_in_blank
# practice_short_answer
# practice_describe_a_photo
# practice_write_down_what_you_hear
# practice_listen_select_real_eng_word
# practice_interactive_conversation
# practice_read_aloud



practice_read_aloud = {
    'practice_id': 10,
    'practice_type': 'read_aloud',
    'practice_name': 'Read the text within 20 seconds ',
    'number_of_questions': 1,
    'limited_time': True,
    'timer': 30,
    'difficulty': 'medium',
    'data': 'Talk about a person you know who inspires you. Who is this person? How do you know this person? Why does this person inspire you?',
    'answer': atob('''We Belong Together" is a classic ballad by Mariah Carey that topped charts around the world upon its release in 2005. The song's soulful vocals and catchy melody struck a chord with listeners, creating a sense of longing and nostalgia that still resonates today. But what many people don't know is that the song almost didn't make it onto Carey's album. According to her producer, Carey had originally recorded the song for a previous album but didn't feel like it fit. It wasn't until she revisited the track years later that she realized its true potential and decided to release it as a single. And the rest, as they say, is history.''')
}


practice_interactive_conversation = {
    'practice_id': 9,
    'practice_type': 'interactive_conversation',
    'practice_name': 'Interactive Conversation',
    'number_of_questions': 4,
    'limited_time': True,
    'timer': 480,
    'difficulty': 'medium',
    'audio': 'https://res.cloudinary.com/detready/video/upload/dictation/Dictation_247.mp3',
    'data': [{
        'id': 1,
        'question': 'What your name',
        'answer': atob('12c'),
        'answer_type': 'select',
        'option': [{
            'id': '12a',
            'value': 'The Rise and Fall of the Roman Empire'
        },{
            'id': '12b',
            'value': 'A Brief History of European Architecture'
        },{
            'id': '12c',
            'value': 'European History: From Ancient Times to the Present Day'
        },{
            'id': '12d',
            'value': 'The Industrial Revolution and Its Impact on Europe'
        }]
    },{
        'id': 2,
        'question': 'Which of the following titles best describes the passage?',
        'answer': atob('2c'),
        'answer_type': 'select',
        'option': [{
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
        'answer_type': 'select',
        'option': [{
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
        'answer': "",
        'answer_type': 'type',
        'option': []
    }]
}


practice_listen_select_real_eng_word = {
    'practice_id': 8,
    'practice_type': 'listen_select_real_eng_word',
    'practice_name': 'Choose Real English Words Only',
    'number_of_questions': 1,
    'limited_time': False,
    'timer': 120,
    'difficulty': 'medium',
    'data': [
        {
            'id': 's1',
            'name': 'unvasivement',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/unvasivement.mp3',
            'answer': atob('incorrect'),
        },
        {
            'id': 's2',
            'name': 'feedback',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/feedback.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's3',
            'name': 'macropapa',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/macropapa.mp3',
            'answer': atob('incorrect'),
        },
        {
            'id': 's4',
            'name': 'monophasement',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/monophasement.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's5',
            'name': 'jurpeting',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/jurpeting.mp3',
            'answer': atob('incorrect'),
        },
        {
            'id': 's6',
            'name': 'helature',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/helature.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's7',
            'name': 'contractor',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/contractor.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's8',
            'name': 'exploit',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/exploit.mp3',
            'answer': atob('incorrect'),
        },
        {
            'id': 's9',
            'name': 'Dictation',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/exploit.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's10',
            'name': 'Dictation',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/exploit.mp3',
            'answer': atob('incorrect'),
        },
        {
            'id': 's11',
            'name': 'Dictation',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/exploit.mp3',
            'answer': atob('correct'),
        },
        {
            'id': 's12',
            'name': 'Dictation',
            'value': 'https://res.cloudinary.com/detready/video/upload/spoken-words/exploit.mp3',
            'answer': atob('correct'),
        }    
    ]
}


practice_write_down_what_you_hear = {
    'practice_id': 7,
    'practice_type': 'write_down_what_you_hear',
    'practice_name': 'Write down what you hear',
    'limited_time': True,
    'timer': 30,
    'difficulty': 'medium',
    'data': 'https://res.cloudinary.com/detready/video/upload/dictation/Dictation_247.mp3',
    'answer': atob('''We Belong Together" is a classic ballad by Mariah Carey that topped charts around the world upon its release in 2005. The song's soulful vocals and catchy melody struck a chord with listeners, creating a sense of longing and nostalgia that still resonates today. But what many people don't know is that the song almost didn't make it onto Carey's album. According to her producer, Carey had originally recorded the song for a previous album but didn't feel like it fit. It wasn't until she revisited the track years later that she realized its true potential and decided to release it as a single. And the rest, as they say, is history.''')
}


practice_describe_a_photo = {
    'practice_id': 6,
    'practice_type': 'describe_a_photo',
    'practice_name': 'Write at least one sentence about the following photo',
    'limited_time': True,
    'timer': 60,
    'difficulty': 'medium',
    'data': 'https://ik.imagekit.io/tvlk/blog/2019/01/shirakawago-1-800x534.jpg?tr=dpr-2,w-675',
    'answer': atob('''We Belong Together" is a classic ballad by Mariah Carey that topped charts around the world upon its release in 2005. The song's soulful vocals and catchy melody struck a chord with listeners, creating a sense of longing and nostalgia that still resonates today. But what many people don't know is that the song almost didn't make it onto Carey's album. According to her producer, Carey had originally recorded the song for a previous album but didn't feel like it fit. It wasn't until she revisited the track years later that she realized its true potential and decided to release it as a single. And the rest, as they say, is history.''')
}


practice_short_answer = {
    'practice_id': 5,
    'practice_type': 'short_answer',
    'practice_name': 'Write at least 50 words on the following topic',
    'limited_time': True,
    'timer': 300,
    'difficulty': 'medium',
    'data': 'What year was "We Belong Together" released?',
    'answer': atob('''We Belong Together" is a classic ballad by Mariah Carey that topped charts around the world upon its release in 2005. The song's soulful vocals and catchy melody struck a chord with listeners, creating a sense of longing and nostalgia that still resonates today. But what many people don't know is that the song almost didn't make it onto Carey's album. According to her producer, Carey had originally recorded the song for a previous album but didn't feel like it fit. It wasn't until she revisited the track years later that she realized its true potential and decided to release it as a single. And the rest, as they say, is history.''')
}




practice_fill_in_blank = {
    'practice_id': 4,
    'practice_type': 'fill_in_blank',
    'practice_name': 'Fill in The Blank',
    'limited_time': True,
    'timer': 180,
    'difficulty': 'medium',
    'data': '''Evolution is a biological process in which all living beings {{0}}{{1}}{{2}}{{3}}{{4}}{{5}} their organism <br> attributes through {{6}}{{7}}{{8}}{{9}}{{10}}{{11}}{{12}} 
            mutations over long {{13}}{{14}}{{15}}{{16}}{{17}}{{18}}{{19}} of time.''',
    'answer': [
        {
            'value': atob('c'),
            'show': True,
        }, {
            'value': atob('h'),
            'show': True,
        }, {
            'value': atob('a'),
            'show': True,
        }, {
            'value': atob('n'),
            'show': False,
        }, {
            'value': atob('g'),
            'show': False,
        }, {
            'value': atob('e'),
            'show': False,
        }, {
            'value': atob('g'),
            'show': True,
        }, {
            'value': atob('e'),
            'show': True,
        }, {
            'value': atob('n'),
            'show': True,
        }, {
            'value': atob('e'),
            'show': False,
        }, {
            'value': atob('t'),
            'show': False,
        }, {
            'value': atob('i'),
            'show': False,
        }, {
            'value': atob('c'),
            'show': False,
        }, {
            'value': atob('p'),
            'show': True,
        }, {
            'value': atob('e'),
            'show': True,
        }, {
            'value': atob('r'),
            'show': True,
        }, {
            'value': atob('i'),
            'show': False,
        }, {
            'value': atob('o'),
            'show': False,
        }, {
            'value': atob('d'),
            'show': False,
        }, {
            'value': atob('s'),
            'show': False,
        }
    ],
}


practice_reading_select_real_eng_word = {
    'practice_id': 3,
    'practice_type': 'reading_select_real_eng_word',
    'practice_name': 'Choose Real English Words Only ',
    'number_of_questions': 1,
    'limited_time': False,
    'timer': 120,
    'difficulty': 'medium',
    'data': [
        {
            'id': 's1',
            'value': 'bird',
            'answer': atob('incorrect'),
        },
        {
            'id': 's2',
            'value': 'bus',
            'answer': atob('correct'),
        },
        {
            'id': 's3',
            'value': 'dot',
            'answer': atob('incorrect'),
        },
        {
            'id': 's4',
            'value': 'giraffe',
            'answer': atob('correct'),
        },
        {
            'id': 's5',
            'value': 'ice cream',
            'answer': atob('incorrect'),
        },
        {
            'id': 's6',
            'value': 'listen',
            'answer': atob('correct'),
        },
        {
            'id': 's7',
            'value': 'monkey',
            'answer': atob('correct'),
        },
        {
            'id': 's8',
            'value': 'papaya',
            'answer': atob('incorrect'),
        },
        {
            'id': 's9',
            'value': 'queen',
            'answer': atob('correct'),
        },
        {
            'id': 's10',
            'value': 'school',
            'answer': atob('incorrect'),
        },
        {
            'id': 's11',
            'value': 'small',
            'answer': atob('correct'),
        },
        {
            'id': 's12',
            'value': 'student',
            'answer': atob('correct'),
        }    
    ]
}


practice_matching = {
    'practice_id': 2,
    'practice_type': 'matching',
    'practice_name': 'Match the right information with the right paragraph',
    'number_of_questions': 1,
    'limited_time': False,
    'timer': 0,
    'difficulty': 'medium',
    'data': [
        {
            'id': 'a1',
            'value': 'Exploring the Ethics of Genetic Modification A In a cutting-edge research institute, a diverse range of subjects are explored, from artificial intelligence to renewable energy. One particular course that stands out is "Genetic Engineering for Enhanced Traits." This course raises some eyebrows, as it delves into the controversial realm of manipulating genetic material to achieve desired characteristics in living organisms. It seems that this research institution is not afraid to push boundaries, but the question arises: is this course a responsible pursuit of knowledge?',
            'answer': atob('b2'),
        },{   
            'id': 'a2',
            'value': 'B This course is aimed at future geneticists and bioengineers, who will learn about the techniques and methods used to modify the genetic makeup of organisms to obtain specific traits. While the primary intention is to advance medical research and develop novel therapies for genetic disorders, there is a potential risk that this knowledge could be misused for purposes such as designer babies or the creation of harmful biological agents. Thus, the course raises ethical concerns about the possible misuse of the knowledge acquired.',
            'answer': atob('b1'),
        },{ 
            'id': 'a3',
            'value': 'C When discussing the ethics of genetic modification with students in this course, the conversation often revolves around the responsibilities and limitations of using this technology. How far should we go in modifying organisms to achieve desired traits, and who should have the authority to decide these limits? These are the questions that arise when considering the morality of genetic engineering.',
            'answer': atob('b3'),
        }
    ],
    'options': [
        {
            'id': 'b1',
            'value': 'Courses that require a high level of commitment',
        },{
            'id': 'b2',
            'value': 'A course title with two meanings',
        },{
            'id': 'b3',
            'value': 'Applying a theory in an unexpected context',
        }
    ]
    
}


practice_reading = {
    'practice_id': 1,
    'practice_type': 'reading',
    'practice_name': 'Interactive Reading : Read the following passage and choose the right answer',
    'number_of_questions': 4,
    'limited_time': True,
    'timer': 480,
    'difficulty': 'medium',
    'data': [{
        'id': 1,
        'question': '''"We Belong Together" is a classic ballad by Mariah Carey that topped charts around the world upon its release in 2005. The song's soulful vocals and catchy melody struck a chord with listeners, creating a sense of longing and nostalgia that still resonates today. But what many people don't know is that the song almost didn't make it onto Carey's album. According to her producer, 

_____________________________________(Missing Sentence)''',
        'answer': atob('1c'),
        'answer_type': 'select',
        'option': [{
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
        'answer_type': 'select',
        'option': [{
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
        'answer_type': 'select',
        'option': [{
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
        'answer': "",
        'answer_type': 'type',
        'option': []
    }]
}






