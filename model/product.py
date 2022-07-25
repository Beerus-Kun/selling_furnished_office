import psycopg2
from .config import database

# def changeInfo(phone, name, gender, email):
#     try:
#         conn = database.conn()
#         cur = conn.cursor()

#         cur.execute('SELECT update_account(%s, %s, %s::int2, %s)', (phone, name, gender, email))
#         # res = cur.fetchone()
#         # res = [dict((cur.description[i][0], value) 
#         #        for i, value in enumerate(row)) for row in cur.fetchall()]
#         # res = dict((cur.description[i][0], value) 
#         #        for i, value in enumerate(cur.fetchone()))
#         cur.close()

#         return res[0]
#     except (Exception, psycopg2.DatabaseError) as error:
#         print(error)
#     finally:
#         if conn is not None:
#             conn.close()

def createProduct(id_category, name, description, quantity, listed_price, image):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT create_product(%s, %s, %s, %s, %s, %s)', (id_category, name, description, quantity, listed_price, image))
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

def updateProduct(id_product, id_category, name, description, quantity, listed_price, image):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT update_product(%s, %s, %s, %s, %s, %s, %s)', (id_product, id_category, name, description, quantity, listed_price, image))
        res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        # return res[0]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getCategories():
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT * from select_category()')
        res = cur.fetchall()
        table = [dict((cur.description[i+1][0], value) 
               for i, value in enumerate(row[1:])) for row in res]
        # res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res[0][0], table
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getProduct(id_category = None):
    try:
        conn = database.conn()
        cur = conn.cursor()

        cur.execute('SELECT * from select_product(%s)', (id_category,))
        # res = cur.fetchall()
        # table = [dict((cur.description[i+1][0], value) 
        #        for i, value in enumerate(row[1:])) for row in res]
        # res = cur.fetchone()
        res = [dict((cur.description[i][0], value) 
               for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
        return -1
    finally:
        if conn is not None:
            conn.close()