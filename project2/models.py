# models.py
import database as db
from utils import extract_user
from flask import session


def curator_info(id):
    curator_info = []
    curator_tags = []

    curator = db.get_query('SELECT * FROM CURATOR WHERE id = ?', (id,), mul=False)
    curator_info.extend([curator[i] for i in range(len(curator))])
    
    ctags = db.get_query('''
                        SELECT TAG.name
                        FROM CURATOR
                        JOIN C_TAG ON CURATOR.id = C_TAG.c_id
                        JOIN TAG ON C_TAG.t_id = TAG.id
                        WHERE CURATOR.id = ?
                        ''', (id,))

    curator_tags.extend([ctags[i]['name'] for i in range(len(ctags))])
    curator_info.append(curator_tags)
    return curator_info


def cu_plyy_tag(id, pid):
    plyy_tags = []
    
    cu_pgtag = db.get_query('''
                SELECT GENRE.name
                FROM GENRE
                JOIN PLYY ON PLYY.g_id = GENRE.id
                WHERE PLYY.c_id = ? and PLYY.id = ?
                ''', (id, pid))
    
    for pgtag in cu_pgtag:
        plyy_tags.append(pgtag['name'])
    
    cu_ptag = db.get_query('''    
            SELECT tag.name
            FROM PLYY
            JOIN P_TAG ON PLYY.id = P_TAG.p_id
            JOIN TAG ON P_TAG.t_id = TAG.id
            WHERE PLYY.c_id = ? and PLYY.id = ?''', (id, pid))

    for t in cu_ptag:
        plyy_tags.append(t['name'])

    return plyy_tags


def cu_plyy(id):
    plyy_list = []

    plyy = db.get_query('SELECT * FROM PLYY WHERE c_id = ?', (id,))

    for p in plyy:  # 플리 객체
        each_plyy = [p[i] for i in range(len(p))]
        each_plyy.append(cu_plyy_tag(id, each_plyy[0]))
        plyy_list.append(each_plyy)

    return plyy_list


def curatorlike_status(cidlist, u_id):
    
    clikestatus = []
    for cid in cidlist:
        likes = db.get_query('SELECT * FROM C_LIKE WHERE c_id = ? and u_id = ?', (cid, u_id),mul=False)
        clikestatus.append(bool(likes))


    return dict(zip(cidlist, clikestatus))


def curator_like(c_id, u_id):
    try:
        row = db.get_query('SELECT * FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id,c_id),mul=False)
        if not row:
            db.execute_query('INSERT INTO C_LIKE (u_id, c_id) VALUES (?, ?)', (u_id, c_id))
        return True
    except Exception as e:
        print(f"Error inserting like: {e}")
        db.roll()
        return False


def curator_unlike(c_id, u_id):
    try:
        row = db.get_query('SELECT * FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id, c_id),mul=False)
        
        if row:
            db.execute_query('DELETE FROM C_LIKE WHERE u_id = ? AND c_id = ?', (u_id, c_id))
        return True
    
    except Exception as e:
        print(f"Error deleting like: {e}")
        db.roll()
        return False


def plyylike_status(pidlist, u_id):
    plikestatus = []
    for pid in pidlist:
        likes = db.get_query('SELECT * FROM P_LIKE WHERE p_id = ? and u_id = ?', (pid, u_id),mul=False)
        plikestatus.append(bool(likes))

    return dict(zip(pidlist, plikestatus))


def plyy_like(p_id, u_id):
    try:
        row = db.get_query('SELECT * FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id),mul=False)
        if not row:
            db.execute_query('INSERT INTO P_LIKE (u_id, p_id) VALUES (?, ?)', (u_id, p_id))

        return True
    
    except Exception as e:
        print(f"Error inserting like: {e}")
        db.roll()
        return False


def plyy_unlike(p_id, u_id):
    try:
        row = db.get_query('SELECT * FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id),mul=False)
        if row:
            db.execute_query('DELETE FROM P_LIKE WHERE u_id = ? AND p_id = ?', (u_id, p_id))
        return True
    
    except Exception as e:
        print(f"Error deleting like: {e}")
        db.roll()
        return False 


def tag_query(category, id, mul=True):
    try:
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
            
        tags = db.get_query(query, (id,), mul)
        
        return tags
    except:
        print('태그 목록을 불러오는데 실패했습니다.')


def plyy_query(condition=None, param=None):
    try:
        query1 = '''
                SELECT
                p.id,
                p.title,
                p.img,
                STRFTIME('%Y-%m-%d', p.gen_date) AS 'generate',
                STRFTIME('%Y-%m-%d', p.up_date) AS 'update',
                c.name AS curator,
                g.name AS genre,
                COUNT(s.num) AS tracks,
                SUM(t.rtime) AS times
                FROM PLYY p
                JOIN CURATOR c ON p.c_id=c.id
                JOIN GENRE g ON p.g_id=g.id
                JOIN SONG s ON p.id=s.p_id
                JOIN TRACK t ON s.tk_id=t.id
                '''
        query2 = ' GROUP BY p.id;'
        
        if condition:
            if condition == 'cid':
                add_query = 'WHERE c.id=?'
            elif condition == 'plyy':
                add_query = "WHERE p.title LIKE '%'||'%';"
            elif condition == 'curator':
                add_query = "WHERE c.name LIKE '%'||'%';"
            query = query1 + add_query + query2
            plyys = db.get_query(query, (param,))


        if not condition:
            query = query1 + query2
            plyys = db.get_query(query)

        result = [dict(row) for row in plyys]


        for i in result:
            tag = tag_query('plyy', i['id'], mul=False)
            if tag:
                tag = dict(tag)
                i['tag'] = tag['name']
            else:
                i['tag'] = ''

        pidlist = [i['id'] for i in result]

        if 'id' in session and session['id']:
            u_id = extract_user(session['id'])
            if u_id:
                p_isliked = plyylike_status(pidlist, u_id)
                print(p_isliked)
                for i in result:
                    i['pliked'] = p_isliked.get(i['id'], False)

        return result
    except:
        print('플레이리스트 목록을 불러오는데 실패했습니다.')
    