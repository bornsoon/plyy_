import database as db
from flask import Blueprint, jsonify, render_template,session
from models import curator_info, curatorlike_status, curator_like, curator_unlike, plyy_like, plyy_unlike, plyylike_status, cu_plyy
from utils import extract_user

main = Blueprint('main', __name__)
plyy = Blueprint('plyy', __name__)
api_main = Blueprint('api_main', __name__)
api_plyy = Blueprint('api_plyy', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@plyy.route('/<id>')
def plyy_detail(id):
    return render_template('plyy.html')


@plyy.route('/<id>/<song_index>')
def song_detail(id, song_index):
    return render_template('song.html')


@api_main.route('/tag')
def api_main_tag():
    query = '''
            SELECT
            name AS tag
            FROM TAG
            UNION
            SELECT
            name AS tag
            FROM GENRE
            '''
    tags = db.get_query(query)
    result = [dict(row) for row in tags]

    return jsonify(result)


@api_main.route('/plyy')
def api_main_plyy():
    try:
        query = '''
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
                GROUP BY p.id;
                '''
        plyys = db.get_query(query)
        result = [dict(row) for row in plyys]

        for i in result:
            tag = db.tag_query('plyy', i['id'], mul=False)
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

    except:
        print('플레이리스트 목록을 불러오는데 실패했습니다.')
    
    return jsonify(result)


@api_main.route('/curator')
def api_main_curator():
    try:
        query = '''
                SELECT
                id,
                name,
                img,
                intro
                FROM CURATOR
                GROUP BY id;
                '''
        curators = db.get_query(query)
        result = [dict(row) for row in curators]
        
        for i in result:
            tags = db.tag_query('curator', i['id'])
            tag = []
            for j in tags[:2]:
                tag.append(j['name'])
            i['tag'] = tag

        date_query = '''
                    SELECT
                    MAX(STRFTIME('%Y-%m-%d', p.gen_date)) AS generate,
                    MAX(STRFTIME('%Y-%m-%d', p.up_date)) AS 'update'
                    FROM PLYY p
                    JOIN CURATOR c ON p.c_id=c.id
                    GROUP BY c.id
                    HAVING c.id=?;
                    '''
        for i in result:
            date = db.get_query(date_query, (i['id'],), mul=False)
            i.update(dict(date))
        
        cidlist = [i['id'] for i in result]

        if 'id' in session and session['id']:
            u_id = extract_user(session['id'])
            if u_id:
                c_isliked = curatorlike_status(cidlist, u_id)
                for i in result:
                    i['cliked'] = c_isliked.get(i['id'], False)
    except:
        print('큐레이터 목록을 불러오는데 실패했습니다.')

    return jsonify(result)


@api_plyy.route('/<id>')
def api_plyy_detail(id):
    try:
        plyy_query = '''
                    SELECT
                    p.title,
                    c.name AS curator, 
                    STRFTIME('%Y-%m-%d', p.gen_date) AS 'generate',
                    STRFTIME('%Y-%m-%d', p.up_date) AS 'update',
                    g.name AS genre,
                    p.cmt AS comment  
                    FROM PLYY p 
                    JOIN CURATOR c ON p.c_id=c.id
                    JOIN GENRE g ON p.g_id=g.id 
                    WHERE p.id=? GROUP BY p.id;
                    '''
        plyy = dict(db.get_query(plyy_query, (id,), mul=False))

        heart_query = '''
                    SELECT
                    COUNT(*) AS heart
                    FROM p_LIKE
                    WHERE p_id=?;
                    '''
        heart = dict(db.get_query(heart_query, (id,), mul=False))
        plyy['heart'] = heart['heart']

        tracks_query = '''
                    SELECT t.id,
                    t.title,
                    t.img,
                    t.album,
                    t.artist,
                    s.num,
                    t.rtime
                    FROM TRACK t 
                    JOIN SONG s ON t.id=s.tk_id
                    JOIN PLYY p ON s.p_id=p.id 
                    WHERE p.id=?;
                    '''
        tracks = db.get_query(tracks_query,(id,))
        tracks = [dict(row) for row in tracks]

        tags = db.tag_query('plyy', id)
        tags = [dict(row) for row in tags]
    except:
        print('해당 플레이리스트의 상세정보 페이지가 존재하지 않습니다.')

    return jsonify({'plyy': plyy, 'tracks': tracks, 'tags': tags})


@api_plyy.route('/<id>/<song_num>')
def api_song(id, song_num):
    try:
        song_query = '''
                    SELECT 
                    t.title,
                    t.artist,
                    t.img,
                    t.album,
                    s.cmt AS comment,
                    s.vid
                    FROM TRACK t 
                    JOIN SONG s ON t.id=s.tk_id 
                    WHERE s.p_id=? AND s.num=?
                    '''
        result = dict(db.get_query(song_query, (id,song_num), mul=False))

        total_query = '''
                    SELECT
                    COUNT(id) AS total
                    FROM SONG
                    WHERE p_id=?
                    '''
        total_index = dict(db.get_query(total_query, (id,), mul=False))

        result['total_num'] = total_index['total']
    except:
        print('해당 곡의 상세정보 페이지가 존재하지 않습니다.')
    
    return jsonify(result)