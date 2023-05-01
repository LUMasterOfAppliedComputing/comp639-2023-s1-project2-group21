import db



def insert(project_title, description, number_of_student, project_type, start_date, end_date, remain_number_of_student):
    sqlCommand = """INSERT INTO project ( project_title, description, number_of_student, project_type,
                     start_date, end_date, remain_number_of_student) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                 % (project_title, description, number_of_student, project_type, start_date, end_date,
                    remain_number_of_student)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def getAll():
    sqlCommand = """SELECT * FROM project """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update(id, project_title, description, number_of_student, project_type, start_date, end_date,
           remain_number_of_student):
    sqlCommand = """UPDATE project SET id = '%s', project_title = '%s',
                     description = '%s', number_of_student = '%s', project_type = '%s', 
                     start_date = '%s', end_date = '%s', remain_number_of_student = '%s' 
                     WHERE id = '%s'""" % (project_title, description,
                                         number_of_student, project_type, start_date, end_date,
                                         remain_number_of_student, id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def delete(id):
    sqlCommand = """DELETE FROM project WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result;
