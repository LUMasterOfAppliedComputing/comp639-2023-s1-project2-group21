import db


def insert(project_id, student_id, rank):
    sqlCommand = """INSERT INTO student_project (project_id, student_id, rank) VALUES ('%s', '%s', '%s')""" % (
    project_id, student_id, rank)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;

def getAll():
    sqlCommand = """SELECT * FROM student_project """
     
    result = db.DBOperator(sqlCommand)
    return result;

def update(project_id, student_id, rank):
    sqlCommand = """UPDATE student_project SET rank= '%s' WHERE project_id = '%s' and student_id = '%s' """ \
                 % (rank, project_id, student_id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(id):
    sqlCommand = """DELETE FROM student_project WHERE project_id = '%s' and student_id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result;

