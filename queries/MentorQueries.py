import db


def insert(mentor_id, phone, summary):
    sqlCommand = """INSERT INTO mentor ( mentor_id, phone, summary)
         VALUES ('%s', '%s', '%s')""" % ( mentor_id, phone, summary)
     
    id = db.DBOperatorInsertedId(sqlCommand)
    return id


def getAll():
    sqlCommand = """SELECT * FROM mentor """
     
    selectResult = db.DBOperator(sqlCommand)
    return selectResult


def update(mentor_id, phone, summary):
    sqlCommand = """UPDATE mentor SET  phone = '%s', summary = '%s' WHERE mentor_id = '%s'"""(phone, summary, mentor_id)
     
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



