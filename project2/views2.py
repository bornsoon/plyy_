import database as db
from flask import Blueprint, jsonify, render_template, request
from models import tag_query, plyy_query, curator_query

main = Blueprint('main', __name__)
plyy = Blueprint('plyy', __name__)
search = Blueprint('search', __name__)
likes = Blueprint('like', __name__)
api_main = Blueprint('api_main', __name__)
api_plyy = Blueprint('api_plyy', __name__)
api_c_plyy = Blueprint('api_c_plyy', __name__)
api_search = Blueprint('api_search', __name__)
api_like = Blueprint('api_like', __name__)


@main.route('/')
def index():
    return render_template('main.html')


@plyy.route('/<id>')
def plyy_detail(id):
    return render_template('plyy.html')


@plyy.route('/<id>/<song_index>')
def song_detail(id, song_index):
    return render_template('song.html')


@search.route('/plyy')
def search_plyy():
    return render_template('search_plyy.html')


@search.route('/curator')
def search_curator():
    return render_template('search_curator.html')


@likes.route('/<id>')
def like(id):
    return render_template('like.html')


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
    result = plyy_query()
    return jsonify(result)


@api_c_plyy.route('/<id>')
def api_curator_plyy(id):
    result = plyy_query('cid', id)
    return jsonify(result)


@api_search.route('/plyy')
def search_plyy():
    param = request.args.get('q')
    if param[0]=='#':
        result = plyy_query('tag', param)
    else:
        result = plyy_query('title', param)
    return jsonify(result)


@api_search.route('/curator')
def search_curator():
    param = request.args.get('q')
    result = curator_query('name', param)
    return jsonify(result)


@api_search.route('/tag')
def search_tag():
    tag = request.args.get('q')
    query = '''
            SELECT
            p.id
            FROM PLYY p
            JOIN P_TAG pt ON p.id=pt.p_id
            WHERE pt.name LIKE '%'||?||'%'
            UNION
            SELECT
            p.id
            FROM PLYY p
            JOIN GENRE g ON p.g_id=g.id
            WHERE pt.name LIKE '%'||?||'%'
            '''
    plyyByTag = db.get_query(query, (tag,))
    result = plyy_query('pid', tag.lower())
    return jsonify(result)


@api_like.route('/plyy/<id>')
def like_plyy(id):
    result = plyy_query('uid', id)
    return jsonify(result)
    

@api_like.route('/curator/<id>')
def like_curator(id):
    result = curator_query('uid', id)
    return jsonify(result)
    

@api_main.route('/curator')
def api_main_curator():
    result = curator_query()
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

        tags = tag_query('plyy', id)
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