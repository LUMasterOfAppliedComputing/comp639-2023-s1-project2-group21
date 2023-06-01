import db


def getStudentMatch():
    sqlCommand = """SELECT
                        sp.student_id,
                        concat(u.first_name,' ',u.last_name),
                        GROUP_CONCAT( DISTINCT sp.project_id ) project_id,
                        GROUP_CONCAT( DISTINCT p.project_title ) p_title,
                            GROUP_CONCAT(  sp.will  )as will
                    FROM
                        student_project sp
                        LEFT JOIN project p ON sp.project_id = p.id
                        LEFT JOIN user u ON u.user_id = sp.student_id
                        left JOIN student stu ON u.user_id = stu.id
                        where stu.placement_status = 0
                    GROUP BY
                        sp.student_id """
    id = db.DBOperator(sqlCommand)
    return id

def getMentorMatch():
    sqlCommand = """SELECT
                        ms.project_id,
                        GROUP_CONCAT(ms.student_id ) as student_id,
                        GROUP_CONCAT( DISTINCT concat(u.first_name,' ',u.last_name)  )as student,
                        GROUP_CONCAT(  ms.will  )as will
                    FROM
                        mentor_student ms
                        LEFT JOIN user u ON u.user_id = ms.student_id
                        left JOIN student stu ON u.user_id = stu.id and stu.placement_status = 0
                    GROUP BY
                        ms.project_id """
    id = db.DBOperator(sqlCommand)
    return id

