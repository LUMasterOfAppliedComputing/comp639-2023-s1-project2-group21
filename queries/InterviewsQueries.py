import db


def insert(project_id, student_id, interview_date, interview_type, interview_status):
    sqlCommand = """INSERT INTO interviews (project_id, student_id, interview_date, interview_type, interview_status)
    VALUES ('%s', '%s', '%s', '%s', '%s')""" % (project_id, student_id, interview_date, interview_type, interview_status)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result


def getAll():
    sqlCommand = """SELECT * FROM interviews """
     
    result = db.DBOperator(sqlCommand)
    return result


def update(project_id, student_id, interview_date, interview_type, interview_status):
    sqlCommand = """UPDATE interviews SET  interview_date = '%s', interview_type = '%s', interview_status = '%s' 
            WHERE project_id= '%s' and student_id = '%s' """ \
                 % (interview_date, interview_type, interview_status, project_id, student_id)
     
    result = db.DBOperator(sqlCommand)
    return result


def delete(id):
    sqlCommand = """DELETE FROM interviews WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result



def update():
    return
