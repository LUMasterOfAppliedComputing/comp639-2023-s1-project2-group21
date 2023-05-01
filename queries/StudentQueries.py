import db



def insert(student_id_no, alternative_name, preferred_name, phone, cv, project_preference,
           personal_statements, placement_status):
    sqlCommand = """INSERT INTO student (id, student_id_no, alternative_name,
                        preferred_name, phone, cv, project_preference,
                        personal_statements, placement_status) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                 % (student_id_no, alternative_name, preferred_name, phone, cv, project_preference, personal_statements,
                    placement_status)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;


def getAll():
    sqlCommand = """SELECT * FROM student """
     
    id = db.DBOperator(sqlCommand)
    return id;


def update(id, company_name, street, city, region, mentor_id, website):
    sqlCommand = """UPDATE student SET student_id_no,alternative_name
                        ,preferred_name,phone,cv,project_preference,
                        personal_statements,placement_status
                        WHERE id = '%s'""" \
                 % (company_name, street, city, region, mentor_id, website, id)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id;


def delete(id):
    sqlCommand = """DELETE FROM student WHERE id = '%s'""" % id
     
    id = db.DBOperator_update(sqlCommand)
    return id;