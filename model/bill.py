import psycopg2
from .config import database

def checkCoupon(code):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT * FROM select_coupon(%s)', (code,))
        res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res[0], res[1]
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def insertCoupon(code, month, value, amount):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT create_coupon(%s, %s, %s, %s)', (code, month, value, amount))
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


# CREATE OR REPLACE function create_bill(
# 	p_phone text,
#     p_name text,
# 	p_email text,
# 	p_address text,
#     -- total
#     p_id_status int,
#     p_id_product int[],
#     p_quantity int[],
#     p_id_coupon text default null
# )

def buy(phone, name, email, address, id_status, id_product, quantity, id_coupon):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT create_bill(%s, %s, %s, %s, %s, %s, %s, %s)', (phone, name, email, address, id_status, id_product, quantity, id_coupon))
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


def check(id_product, quantity, id_coupon):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT check_bill(%s, %s, %s)', (id_product, quantity, id_coupon))
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

def histBill(phone):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT * from select_bill(%s)', (phone,))
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

def histProductBill(idBill):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT * from select_product_bill(%s)', (idBill,))
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

def customerCancel(idBill, phone):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT cancel_bill(%s, %s)', (idBill, phone))
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


def billStatus(status):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT * from manager_select_bill(%s)', (status,))
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

def forceCancel(idBill):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT manager_cancel_bill(%s)', (idBill, ))
        res = cur.fetchone()
        # res = [dict((cur.description[i][0], value) 
        #        for i, value in enumerate(row)) for row in cur.fetchall()]
        # res = dict((cur.description[i][0], value) 
        #        for i, value in enumerate(cur.fetchone()))
        cur.close()

        return res
    except (Exception, psycopg2.DatabaseError) as error:
        print(error)
    finally:
        if conn is not None:
            conn.close()

def nextStep(idBill):
    try:
        conn = database.conn()
        cur = conn.cursor()
        # update_product(id_product, id_category, name, discription, quantity, listed_price, arr image)
        cur.execute('SELECT manager_next_step_bill(%s)', (idBill, ))
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