import sqlite3

DB = './plyy.db'

def get_db_connection():
    conn = sqlite3.connect(DB)
    conn.row_factory = sqlite3.Row

    return conn


def get_query(query, params=None, mul=True):
    conn = get_db_connection()
    cur = conn.cursor()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)

    if mul == True:
        result = cur.fetchall()
    else:
        result = cur.fetchone()

    conn.close()

    return result


def execute_query(query, params):
    conn = get_db_connection
    cur = conn.cursor()
    cur.execute(query, params)
    conn.commit()
    conn.close