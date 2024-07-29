import database as db
import pandas as pd
from flask import Blueprint, jsonify, render_template

main = Blueprint('main', __name__)
plyy = Blueprint('plyy', __name__)
api_main = Blueprint('api_main', __name__)
api_plyy = Blueprint('api_plyy', __name__)


@main.route('/')
def index():
    return render_template('index.html')


@plyy.route('/<id>')
def plyy(id):
    return render_template('plyy.html')


@plyy.route('/<id>/<song_index>')
def song(id, song_index):
    return render_template('song.html')


@api_main.route('/plyy')
def api_main_plyy():
    query = '''
            SELECT
            p.plyy_uuid,
            p.plyy_title,
            p.plyy_img,
            p.plyy_gen_date AS generate,
            p.plyy_update_date AS 'update',
            c.c_name AS curator,
            g.gtag_name AS genre,
            COUNT(s.song_index) AS tracks,
            SUM(t.track_rtime) AS times
            FROM PLYY p
            JOIN CURATOR c ON p.c_uuid=c.c_uuid
            JOIN TAG_GENRE g ON p.gtag_uuid=g.gtag_uuid
            JOIN SONG s ON p.plyy_uuid=s.plyy_uuid
            JOIN TRACK t ON s.track_uuid=t.track_uuid
            GROUP BY p.plyy_uuid;
            '''
    plyys = db.get_query(query)

    for i in plyys:
        i['tags'] = db.tag_query('plyy', i['plyy_uuid'])
    
    return jsonify(plyys)


@api_main.route('/curator')
def api_main_curator():
    query = '''
            SELECT
            c_uuid,
            c_name,
            c_img,
            c_intro
            FROM CURATOR
            GROUP BY c_uuid;
            '''
    curators = db.get_query(query)
    
    for i in curators:
        i['tags'] = db.tag_query('curator', i['c_uuid'])

    date_query = '''
                 SELECT
                 MAX(p.plyy_gen_date) AS generate,
                 MAX(p.plyy_update_date) AS 'update'
                 FROM PLYY p
                 JOIN CURATOR c ON p.c_uuid=c.c_uuid
                 GROUP BY c.c_uuid
                 '''
    date = db.get_query(date_query)
    
    for i in date:
        i['max_date'] = [pd.to_datetime(i['generate']), pd.to_datetime(i['update'])].max()

    return jsonify(curators)


@api_plyy.route('/<id>')
def api_plyy_detail(id):
    # 쿼리문의 복잡도 줄임 (줄바꿈, 인덴트)
    info_query = '''
                 SELECT
                 p.plyy_title,
                 c.c_name AS curator, 
                 strftime('%Y-%m-%d', plyy_gen_date) AS 'generate',
                 strftime('%Y-%m-%d', plyy_update_date) AS 'update',
                 COUNT(*) AS heart,
                 g.gtag_name AS genre,
                 plyy_cmt AS comment  
                 FROM PLYY p 
                 JOIN CURATOR c ON p.c_uuid=c.c_uuid
                 JOIN PLYY_LIKE pl ON p.plyy_uuid=pl.plyy_uuid
                 JOIN TAG_GENRE g ON p.gtag_uuid=g.gtag_uuid 
                 WHERE p.plyy_uuid=? GROUP BY p.plyy_uuid;
                 '''
    info = db.get_query(info_query,(id,),mul=False)
    if info['update'] is None:
        info['update'] = info['generate']

    tracks_query = '''
                   SELECT t.track_uuid,
                   t.track_title AS title,
                   SUBSTR(t.track_album_img,6) AS img,
                   t.track_album AS album,
                   t.track_artist AS artist,
                   s.song_index,
                   t.track_rtime
                   FROM TRACK t 
                   JOIN SONG s ON t.track_uuid=s.track_uuid
                   JOIN PLYY p ON s.plyy_uuid=p.plyy_uuid 
                   WHERE p.plyy_uuid=?;
                   '''
    tracks = db.get_query(tracks_query,(id,))

    tags = db.tag_query('plyy', id)

    return jsonify({'info': info, 'tracks': tracks, 'tags': tags})


@api_plyy.route('/<id>/<song_index>')
def api_song(id, song_index):
    song_query = '''
                 SELECT 
                 t.track_title AS title,
                 t.track_artist as artist,
                 SUBSTR(t.track_album_img,6) AS img,
                 t.track_album AS album,
                 s.song_cmt AS comment,
                 s.song_vid
                 FROM TRACK t 
                 JOIN SONG s ON t.track_uuid=s.track_uuid 
                 WHERE s.plyy_uuid=? AND s.song_index=?
                 '''
    song = db.get_query(song_query, (id,song_index), mul=False)

    total_query = '''
                  SELECT
                  COUNT(song_uuid) AS total
                  FROM SONG
                  WHERE plyy_uuid=?
                  '''
    total_index = db.get_query(total_query, (id,), mul=False)

    song['total_index'] = total_index['total']
    print(song)
    
    return jsonify(song)


if __name__=='__main__':
    app.run(debug=True)