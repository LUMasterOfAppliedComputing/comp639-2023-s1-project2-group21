import db



def insert(student_id, skill_id):
    sqlCommand = """INSERT INTO student_skills ( student_id, skill_id) VALUES ('%s', '%s')""" \
                 % (student_id, skill_id)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAll():
    sqlCommand = """SELECT * FROM student_skills """
     
    result = db.DBOperator(sqlCommand)
    return result


def delete(student_id, skill_id):
    sqlCommand = """DELETE FROM student_skills WHERE student_id = '%s' and skill_id = '%s'""" %(student_id, skill_id)
     
    result = db.DBOperator_update(sqlCommand)
    return result
