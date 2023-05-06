import db


def insert(id, student_id_no, alternative_name, preferred_name, phone, cv, project_preference,
           personal_statements, placement_status, gender, dob):
    sqlCommand = """INSERT INTO student (id, student_id_no, alternative_name,
                        preferred_name, cv, project_preference,
                        personal_statements, placement_status,phone,gender,dateofbirth) VALUES ('%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s', '%s')""" \
                 % (id, student_id_no, alternative_name, preferred_name, cv, project_preference, personal_statements,
                    placement_status, phone, gender, dob)

    newId = db.DBOperatorInsertedId(sqlCommand)
    return newId;


def getAll():
    sqlCommand = """SELECT * FROM student """

    id = db.DBOperator(sqlCommand)
    return id;


def getOneById(id):
    sqlCommand = """SELECT * FROM user where user_id = '%s' """ % (id)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


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


def getStudentByStudentNo(studentNo):
    sqlCommand = """SELECT * FROM student where student_id_no = '%s' """ % (studentNo)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def getStudentById(id):
    sqlCommand = """SELECT
                        *
                    FROM
                        student stu
                        LEFT JOIN user u ON u.user_id = stu.id
                    WHERE
                        u.role = 2 and stu.id = %s """ % (id)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult
