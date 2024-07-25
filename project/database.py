import sqlite3

DB = '../Gen/db/plyy.db'

def connect_db():
    conn = sqlite3.connect(DB)
    conn.execute('PRAGMA foreign_keys = ON')
    conn.row_factory = sqlite3.Row
    cur = conn.cursor()

    return conn, cur


def get_query(query, params=None, mul=True):
    conn, cur = connect_db()

    if params:
        cur.execute(query, params)
    else:
        cur.execute(query)
        
    if mul:
        result = cur.fetchall()
        result = [dict(row) for row in result]
    else:
        result = cur.fetchone()
        result = dict(result)


    conn.close()

    return result


def execute_query(query, params):
    conn, cur = connect_db()
    cur.execute(query, params)
    conn.commit()
    conn.close
