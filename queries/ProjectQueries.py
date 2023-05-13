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

def getProjectAll(ids):
    sqlCommand = """SELECT p.id,p.project_title,p.description,
                    p.number_of_student,pt.type_name,  DATE_FORMAT(p.start_date, '%M %d %Y') as start_date,
                    DATE_FORMAT(p.end_date, '%M %d %Y') as end_date,p.remain_number_of_student,co.company_name 
                    FROM
                        project p
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id
                        LEFT JOIN project_type pt on pt.type_id =p.project_type
                """
    if ids:
        sqlCommand += """ where p.id in (%s)""" % ids

    selectResult = db.DBOperator(sqlCommand)
    return selectResult
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
