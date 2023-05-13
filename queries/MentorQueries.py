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

def updatecompany(company_name, region,city,street,website,companyid):
    sqlCommand ="""
        UPDATE company
        SET company_name = '%s', region = '%s',city = '%s', street = '%s',  website = '%s'
        WHERE id = '%s'
        """%(company_name, region,city,street,website,companyid)
    updateid = db.DBOperator_update(sqlCommand)
    print(updateid)
    return updateid



def getMentorinfo(userid):
    sqlCommand = """SELECT * FROM mentor m  join user u on m.mentor_id = u.user_id where u.user_id = '%s' """ % userid
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult

def getProjectAll():
    sqlCommand = """SELECT p.id,p.project_title,p.description,
                    p.number_of_student,pt.type_name,  DATE_FORMAT(p.start_date, '%M %d %Y') as start_date,
                    DATE_FORMAT(p.end_date, '%M %d %Y') as end_date,p.remain_number_of_student,co.company_name 
                    FROM
                        project p
                        INNER JOIN mentor ON p.mentor_id = mentor.mentor_id
                        LEFT JOIN company co ON co.id = mentor.company_id
                        LEFT JOIN project_type pt on pt.type_id =p.project_type
                """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult