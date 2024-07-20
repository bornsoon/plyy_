import database as db
from flask import Flask, jsonify, json

app = Flask(__name__)


@app.route('/')
def index():
    return app.send_static_file('index.html')


@app.route('/api/plyy')
def plyy():
    info_query = '''
            SELECT p.plyy_title AS title, c.c_name AS curator, strftime('%Y-%m-%d', plyy_gen_date) AS generate,
            strftime('%Y-%m-%d', plyy_update_date) AS 'update', COUNT(pl.plyy_uuid) AS heart, g.gtag_name AS Genre, plyy_cmt AS comment  
            FROM PLYY p JOIN CURATOR c ON p.c_uuid=c.c_uuid JOIN PLYY_LIKE pl ON p.plyy_uuid=pl.plyy_uuid
            JOIN TAG_GENRE g ON p.gtag_uuid=g.gtag_uuid GROUP BY p.plyy_uuid;
            '''
    info = db.get_query(info_query)

    plyy_query = '''
                SELECT t.track_title AS title, t.track_album_img AS img, t.track_album AS album, t.track_artist AS artist
                FROM TRACK t JOIN SONG s ON t.track_uuid=s.track_uuid JOIN PLYY p ON s.plyy_uuid=p.plyy_uuid;
                '''
    plyy = db.get_query(plyy_query)
        
    return jsonify(info, plyy)


@app.route('/api/plyyList')
def plyyList():
    return app.send_static_file('plyy.html')


if __name__=='__main__':
    app.run(debug=True)