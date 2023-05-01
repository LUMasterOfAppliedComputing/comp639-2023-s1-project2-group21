import db


def insert(first_name: object, last_name: object, password: object, email: object, role: object) -> object:
    sqlCommand = """INSERT INTO user ( first_name, last_name, password, email, role)
         VALUES ('%s', '%s', '%s', '%s', '%s')""" % (
        first_name, last_name, password, email, role)
    result = db.DBOperatorInsertedId(sqlCommand)
    return result


def getAll():
    sqlCommand = """SELECT * FROM user"""
    result = db.DBOperator(sqlCommand)
    return result


def update(id, first_name, last_name, password, email, role):
    sqlCommand = """UPDATE user SET first_name = '%s', last_name = '%s', 
                  password = '%s', email = '%s',  role = '%s' WHERE user_id = '%s' """%(first_name, last_name, password, email, role,id)
     
    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult


def delete(id):
    sqlCommand = """DELETE FROM user WHERE user_id = '%s'""" % id
    selectResult = db.DBOperator_update(sqlCommand)
    return selectResult


def getUserByEmail(email, role):
    sqlCommand = """SELECT * FROM user where email = '%s' and role ='%s' """ % (email, role)
    selectResult = db.DBOperator(sqlCommand)
    return selectResult
