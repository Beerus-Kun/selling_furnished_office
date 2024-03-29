import psycopg2
from .config import database

# create_account(username, password, id_role, name, gender, email, phone)


def createCustomerAccount(username, password, name, gender, email, phone, address):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT create_account(%s, %s, %s, %s, %s::int2, %s, %s, %s);", (username, password.decode("utf-8"), 3, name, gender, email, phone, address))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def createTempCustomer(phone):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT create_temp_customer(%s);", (phone,))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def createStaffAccount(username, password, name, gender, email):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT create_account(%s, %s, %s, %s, %s::int2, %s)', (username, password.decode("utf-8"), 2, name, gender, email))

        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def restoreStaffAccount(username, password):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute("""
            update account
            set password = %s
            where username = %s
         """, (password.decode("utf-8"), username))

        # res = cur.fetchone()
        cur.close()
        # return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def updateStaff(name, gender, email):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute("""
            update staff
            set name = %s, gender = %s::int2
            where email = %s
         """, (name, gender, email))

        # res = cur.fetchone()
        cur.close()
        # return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def deleteStaff(username):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute("""
            update account
            set password = null
            where username = %s
         """, (username,))

        # res = cur.fetchone()
        cur.close()
        # return res[0]
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

def getStaff(username):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT * from staff where username = %s', (username,))

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
# select *, a.password is null as status
# from account a, staff s
# where a.username = s.username
def selectStaff():
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute(""" 
        select *, a.password is null as status
            from account a, staff s
            where a.username = s.username
            
        """)
        # res = cur.fetchone()
        res = [dict((cur.description[i][0], value) 
               for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def statusStaff(username):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute(""" 
            select password is null as status
            from account 
            where username = %s
        """,(username,))
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

        cur.execute('SELECT update_password(%s, %s)', (username, password.decode("utf-8")))
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


def checkPhone(phone):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT check_phone(%s);", (phone,))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def checkEmail(email):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT check_email(%s);", (email,))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()


def checkUsername(username):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute("SELECT check_username(%s);", (username,))
        res = cur.fetchone()
        cur.close()
        return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()