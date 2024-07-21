import database as db
from flask import Flask, jsonify, json

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/plyy')
def plyy():
    api_plyy()
    return app.send_static_file('index.html')


@app.route('/plyy/<id>')
def plyy_detail(id):
    api_plyy_detail(id)
    return app.send_static_file('index.html')


@app.route('/api/plyy')
def api_plyy():
    query = '''
            SELECT plyy_uuid, plyy_title FROM PLYY;
            '''
    plyyList = db.get_query(query)
    return jsonify(plyyList)


@app.route('/api/plyy/<id>')
def api_plyy_detail(id):
    print(id)
    info_query = '''
                SELECT p.plyy_uuid, p.plyy_title, c.c_name AS curator, strftime('%Y-%m-%d', plyy_gen_date) AS generate,
                strftime('%Y-%m-%d', plyy_update_date) AS 'update', COUNT(pl.plyy_uuid) AS heart, g.gtag_name AS Genre, plyy_cmt AS comment  
                FROM PLYY p JOIN CURATOR c ON p.c_uuid=c.c_uuid JOIN PLYY_LIKE pl ON p.plyy_uuid=pl.plyy_uuid
                JOIN TAG_GENRE g ON p.gtag_uuid=g.gtag_uuid WHERE p.plyy_uuid=? GROUP BY p.plyy_uuid;
                '''
    info = db.get_query(info_query,(id,),mul=False)
    if info['update'] is None:
        info['update'] = info['generate']

    return jsonify(info)


@app.route('/api/trackList')
def api_trackList(id):   
    trackList_query = '''
                    SELECT t.track_title, t.track_album_img AS img, t.track_album AS album, t.track_artist AS artist
                    FROM TRACK t JOIN SONG s ON t.track_uuid=s.track_uuid JOIN PLYY p ON s.plyy_uuid=p.plyy_uuid WHERE p.plyy_uuid=?;
                    '''
    tracks = db.get_query(trackList_query,(id,))
        
    return jsonify(tracks)


if __name__=='__main__':
    app.run(debug=True)