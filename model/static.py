import psycopg2
from .config import database

def monthTurnover(date):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from month_turnover(%s)', (date,))
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

def totalMonthTurnover(date):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT total_month_turnover(%s)', (date,))
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


def yearTurnover(date):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from year_turnover(%s)', (date,))
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

def totalYearTurnover(date):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT total_year_turnover(%s)', (date,))
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

def monthStatus(date):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from month_status(%s)', (date,))
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

def getBoughtBill(start, stop):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from admin_select_bill(%s, %s)', (start, stop))
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

def getTotalBill(start, stop):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute("""
            select sum(b.total)
        from bill b
        where b.id_status = 5 and b.date_time::date>=%s and b.date_time::date<=%s
         """, (start, stop))
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

def adminYear():
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from get_admin_year()')
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

def adminMonth(year):
    try:
        conn = database.conn()
        cur = conn.cursor()
        cur.execute('SELECT * from get_admin_month(%s)', (year, ))
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