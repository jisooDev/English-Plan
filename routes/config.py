from . import *

blueprintConfig = Blueprint('config', __name__)

@blueprintConfig.route('/config')
def render_selectword():
    connection = query.get_connection()
    cursor = connection.cursor()

    sql_str = '''
        SELECT practice_id ,practice_merge , practice_type , practice_name , limited_time , timer FROM exam_config
    '''
    cursor.execute(sql_str)
    response = cursor.fetchall()

    return render_template('admin/pages/config/config.html' , response=response)