import psycopg2
from .config import database

# p_username text,
# 	p_password text,
# 	p_name text,
# 	p_id_role integer,
# 	p_gender smallint default null,
# 	p_email text default null,
# 	p_phone text default null

def createCustomerAccount(username, password, name, id_role, gender, email, phone):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT create_account(%s, %s, %s, %s, %s, %s, %s)', (username, password, name, id_role, gender, email, phone))

        res = cur.fetchone()
        cur.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def createStaffAccount(username, password, name, id_role):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT create_account(%s, %s, %s, %s)', (username, password, name, id_role))

        res = cur.fetchone()
        cur.close()
        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

