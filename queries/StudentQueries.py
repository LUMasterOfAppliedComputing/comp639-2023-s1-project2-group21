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
    sqlCommand = """SELECT
                        user_id as id,
                        first_name,
                        last_name,
                        student_id_no,
                        phone,
                        email,
                        GROUP_CONCAT(tk.skill_name) as skill,
                        cv 
                    FROM
                        student stu
                        LEFT JOIN USER u ON u.user_id = stu.id 
                        LEFT JOIN student_skills sk on stu.id = sk.student_id
                        LEFT JOIN techs_and_skills tk on tk.id = skill_id
                    WHERE
                        u.role = 2  GROUP BY user_id"""

    id = db.DBOperator(sqlCommand)
    return id;


def getOneById(id):
    sqlCommand = """SELECT * FROM user where user_id = '%s' """ % (id)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def update(id, alternative_name, preferred_name, phone, cv, project_preference, personal_statements, dob):
    sqlCommand = """UPDATE student set alternative_name ='%s'
                        ,preferred_name ='%s',phone ='%s',cv='%s',project_preference='%s',
                        personal_statements='%s',dateofbirth='%s'
                        WHERE id = '%s'""" % (
    alternative_name, preferred_name, phone, cv, project_preference, personal_statements, dob, id)
    print(sqlCommand)
    id = db.DBOperator_update(sqlCommand)
    return id;


def updatePlacementStatus(id, placement_status):
    sqlCommand = """UPDATE student set placement_status='%s'
                        WHERE id = '%s'""" % ( placement_status, id)
    print(sqlCommand)
    id = db.DBOperator_update(sqlCommand)
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


def getAllRanked(pid):
    sqlCommand = """SELECT
                        sp.rank,
                        user_id AS id,
                        first_name,
                        last_name,
                        student_id_no,
                        phone,
                        email,
                        GROUP_CONCAT( tk.skill_name ) AS skill,
                        cv
                    FROM
                        student stu
                        LEFT JOIN USER u ON u.user_id = stu.id
                        LEFT JOIN student_skills sk ON stu.id = sk.student_id
                        LEFT JOIN techs_and_skills tk ON tk.id = skill_id
                        LEFT JOIN student_project sp on sp.student_id = user_id and sp.project_id ='%s'
                    WHERE
                        u.role = 2 
                    GROUP BY
                        user_id
                    ORDER BY (CASE WHEN sp.rank IS NULL THEN 99 ELSE sp.rank END), sp.rank ASC """ % (pid)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult