import db

def addwishlist(project_id, userId):
    sqlCommand = """INSERT INTO wishlist ( project_id, student_id) VALUES ('%s', '%s')""" % (project_id, userId)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result

def removewishlist(project_id, userId):
    sqlCommand = """DELETE FROM wishlist WHERE project_id = '%s' and student_id = '%s'""" % (project_id, userId)
     
    result = db.DBOperator_update(sqlCommand)
    return result

def showwishlist(userId):
    sqlCommand ="""SELECT * FROM (project p join wishlist w on w.project_id =p.id) join student s on w.student_id=s.id where s.id='%s'"""% (userId)

    result = db.DBOperator(sqlCommand)
    return result