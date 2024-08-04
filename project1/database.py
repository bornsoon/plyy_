import sqlite3
import os

def connect_db():
    database_path = os.path.join(os.path.dirname(__file__), 'plyy_v4.db')
    conn = sqlite3.connect(database_path)
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
    else:
        result = cur.fetchone()

    conn.close()

    return result


def execute_query(query, params):
    conn, cur = connect_db()
    cur.execute(query, params)
    conn.commit()
    conn.close


def tag_query(category, id, mul=True):
    if category.lower() == 'plyy':
        query = '''
                SELECT
                t.name 
                FROM TAG t 
                JOIN P_TAG pt ON t.id=pt.id
                WHERE pt.p_id=?
                '''

    elif category.lower() == 'curator':
        query = '''
                SELECT
                t.name
                FROM TAG t
                JOIN C_TAG ct ON t.id=ct.id
                WHERE ct.c_id=?
                '''
        
    tags = get_query(query, (id,), mul)
    
    return tags

def roll():
    conn,cur = connect_db()
    conn.rollback()
    conn.close()