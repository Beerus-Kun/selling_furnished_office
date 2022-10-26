import psycopg2
from .config import database


def insertComment(username, idProduct, content):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT create_comment(%s, %s, %s)', (username, idProduct, content))
        # res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        # return res[0], res[1]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def getComment(idProduct):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT * from select_comment(%s)', (idProduct, ))
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