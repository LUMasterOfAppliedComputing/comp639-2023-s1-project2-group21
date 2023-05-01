import db


def insert(project_id, skill_id):
    sqlCommand = """INSERT INTO project_skills (project_id, skill_id) VALUES ('%s', '%s')""" % (project_id, skill_id)
     
    result = db.DBOperatorInsertedId(sqlCommand)
    return result;


def getAll():
    sqlCommand = """SELECT * FROM project_skills """
     
    result = db.DBOperator(sqlCommand)
    return result;


def update():
    return """UPDATE project_skills WHERE id = '%s'"""


def delete(project_id, skill_id):
    sqlCommand = """DELETE FROM project_skills WHERE project_id = '%s' and skill_id = '%s' """ % (project_id, skill_id)
     
    result = db.DBOperator_update(sqlCommand)
    return result;

