import psycopg2
from .config import database

# create_account(username, password, id_role, name, gender, email, phone)


def createCustomerAccount(username, password, name, gender, email, phone):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT create_account(%s, %s, %s, %s, %s::int2, %s, %s);", (username, password.decode("utf-8"), 3, name, gender, email, phone))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def createStaffAccount(username, password):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT create_account(%s, %s, %s)', (username, password.decode("utf-8"), 2))

        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getAccount(username):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT * from select_account(%s)', (username,))

        res = dict((cur.description[i][0], value) 
               for i, value in enumerate(cur.fetchone()))
        cur.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getPassword(username):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT * from select_password(%s)', (username,))
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        res = dict((cur.description[i][0], value) 
               for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def changeInfo(phone, name, gender, email):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT update_account(%s, %s, %s::int2, %s)', (phone, name, gender, email))
        res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def changePassword(username, password):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT update_password(%s, %s)', (username, password))
        res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()