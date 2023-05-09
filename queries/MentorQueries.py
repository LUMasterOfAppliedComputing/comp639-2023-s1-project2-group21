import db


def insert(mentor_id, phone, summary,cid):
    sqlCommand = """INSERT INTO mentor ( mentor_id, phone, summary,company_id)
         VALUES ('%s', '%s', '%s', '%s')""" % ( mentor_id, phone, summary,cid)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAll():
    sqlCommand = """
                    SELECT
                        *
                    FROM
                        mentor m
                        LEFT JOIN company c ON m.company_id = c.id
                        LEFT JOIN user u ON u.user_id = m.mentor_id
                    WHERE
                        u.role =1
                """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def update(mentor_id, phone, summary):
    sqlCommand = """UPDATE mentor SET  phone = '%s', summary = '%s' WHERE mentor_id = '%s'""" % (phone, summary, mentor_id)
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def delete(id):
    sqlCommand = """DELETE FROM mentor WHERE mentor_id = '%s'""" % id
     
    deleteResult = db.DBOperator_update(sqlCommand)
    return deleteResult

def getMentorinfo(userid):
    sqlCommand = """SELECT * FROM mentor m  join user u on m.mentor_id = u.user_id where u.user_id = '%s' """ % userid
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def getProjectAll():
    sqlCommand = """
                    SELECT
                        *,c.company_name as company_name
                    FROM
                        project p inner join company c on p.company_id = c.id
                """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult