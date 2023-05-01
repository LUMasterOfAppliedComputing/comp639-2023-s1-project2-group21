import db



def insert(question):
    sqlCommand = """INSERT INTO question (question) VALUES ( '%s')""" % question
     
    id = selectResult = db.DBOperator(sqlCommand)
    return id;

def getAll():
    sqlCommand = """SELECT * FROM question """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update(id, question):
    sqlCommand = """UPDATE question SET  question = '%s' WHERE id = '%s'""" % (question, id)
     
    result = db.DBOperator(sqlCommand)
    return result;


def delete(id):
    sqlCommand = """DELETE FROM question WHERE id = '%s'""" % id
     
    result = db.DBOperator_update(sqlCommand)
    return result;
