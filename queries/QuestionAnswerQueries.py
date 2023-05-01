import db

table_name = "t_question_answer"


def insert(student_id, question_id, question_answer):
    sqlCommand = """INSERT INTO question_answer (student_id, question_id, question_answer) VALUES ('%s', '%s', '%s')""" % (
        student_id, question_id, question_answer)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;


def getAll():
    sqlCommand = """SELECT * FROM question_answer """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update(student_id, question_id, question_answer):
    sqlCommand = """UPDATE question_answer SET  question_answer = '%s' WHERE student_id = '%s' and question_id = '%s' """ \
                 % (student_id, question_id, question_answer)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(student_id, question_id):
    sqlCommand = """DELETE FROM question_answer WHERE student_id = '%s' and question_id = '%s'  """ % (
    student_id, question_id)
     
    result = db.DBOperator_update(sqlCommand)
    return result;
