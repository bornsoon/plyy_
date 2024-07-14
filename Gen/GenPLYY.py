from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from Gen.OutputFile import  OutputDict

cid = '4a07e98721c84fcab2458d5813965796'
secret = '9fc833bbc4a647c8b56ddb3e952d04b4'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')


def spotify_plyy_src(playlist_id):
    result = sp.playlist_tracks(playlist_id, additional_types=("track",))
    plyy_result = []
    for i in result['items']:
        l = i['track']
        albumImg = [Img for Img in l['album']['images'] if Img['height'] == 640][0]['url']
        artist = ','.join([art['name'] for art in l['artists']])
        plyy_result.append({'Id': l['id'], 'Title': l['name'], 'Artist': artist, 'Album': l['album']['name'], 'AlbumImg': albumImg})
    return plyy_result


def songToCsv(playlist_id):
    song_result = []
    plyy = spotify_plyy_src(playlist_id)
    for i in plyy:
        song_result.append({'Id': 'song_'+ i['Id'], 'Vidoe': '', 'PlyyId': playlist_id, 'SrcId': i['Id']})
    return song_result


def srcToCsv(playlist_id):
    plyy = spotify_plyy_src(playlist_id)
    OutputDict(plyy, 'plyy_' + playlist_id + '.csv')
    

if __name__=='__main__':
    playlist_id = ['37i9dQZF1DWT9uTRZAYj0c',
                   '37i9dQZF1DXbShqaetC9Tw',
                   '37i9dQZF1DWSvk1AxYsbvo',
                   '37i9dQZF1DWZiWafrEIdA8',
                   '37i9dQZF1DX3NfV1mHBR08',
                   '37i9dQZF1DWUYWXTlNjc6T',
                   '37i9dQZF1DX5g856aiKiDS',
                   '37i9dQZF1DX5LEXW9eXA0n',
                   '37i9dQZF1DX2ohL85TE8TI']
    for i in playlist_id:
        srcToCsv(i)
        songToCsv(i)