import connect, mysql.connector
connection = None
dbconn = None

def DBConnect():
    global dbconn
    global connection
    if dbconn == None:
        connection = mysql.connector.connect(user=connect.dbuser, password=connect.dbpass, host=connect.dbhost,
                                             database=connect.dbname, autocommit=True,buffered=True)
        dbconn = connection.cursor()
        return dbconn
    else:
        if connection.is_connected():
            return dbconn
        else:
            connection = None
            dbconn = None
            return DBConnect()


def DBOperator(sqlCommands):
    """

    :rtype: object
    """
    cur = DBConnect()
    rows_affected = cur.execute(sqlCommands)
    if(cur.with_rows == False):
        return []
    select_result = cur.fetchall()
    column_names = [i[0] for i in cur.description]
    return [dict(zip(column_names, row)) for row in select_result]
  #  return select_result

def DBOperatorInsertedId(sqlCommands):
    cur = DBConnect()
    cur.execute(sqlCommands)
    select_result = cur.lastrowid
    return select_result


def DBOperatorFetchOne(sqlCommands):
    cur = DBConnect()
    cur.execute(sqlCommands)
    select_result = cur.fetchone()
    return select_result

def DBOperator_search(sqlCommands,searchtext_tuple):
    cur = DBConnect()
    rows_affected = cur.execute(sqlCommands,searchtext_tuple)
    if(cur.with_rows == False):
        return []
    select_result = cur.fetchall()
    return select_result

def DBOperator_update(sqlCommands):
    cur = DBConnect()
    rows_affected = cur.execute(sqlCommands)
    return rows_affected