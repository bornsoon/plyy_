from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
from Gen.OutputFile import OutputFile, OutputDict
from dotenv import load_dotenv
import os

load_dotenv()

OWM_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

cid = os.getenv('SPOTIFY_CID')
secret = os.getenv('SPOTIFY_SECRET')
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')

def track(artist, title):
    result = sp.search(title + artist, limit=1)
    rslt = result['tracks']['items'][0]
    albumTitle = rslt['album']['name']
    albumImg = [Img for Img in rslt['album']['images'] if Img['height'] == 640][0]['url']
    artist = ','.join([art['name'] for art in rslt['artists']])
    srcTitle = rslt['name']
    srcId = rslt['id']

    src = {'Id': srcId, 'Title': srcTitle, 'Artist': artist, 'Album': albumTitle, 'AlbumImg': albumImg}

    return src


def spotify_plyy(playlist_id):
    result = sp.playlist_tracks(playlist_id, additional_types=("track",))
    plyy_result = []
    for i in result['items']:
        l = i['track']
        albumImg = [Img for Img in l['album']['images'] if Img['height'] == 640][0]['url']
        artist = ','.join([art['name'] for art in l['artists']])
        plyy_result.append({'Id': l['id'], 'Title': l['name'], 'Artist': artist, 'Album': l['album']['name'], 'AlbumImg': albumImg})
    return plyy_result


def plyyToCsv(playlist_id):
    plyy = spotify_plyy(playlist_id)
    OutputDict(plyy, 'plyy_' + playlist_id + '.csv')
    

if __name__=='__main__':
    print(track('케이윌', '체리블라썸'))
    # print(track('로꼬', 'say yes'))
    # print(track('펀치', 'say yes'))
    # OutputFile(str(plyy), 'spotipy_playlist_tracks.txt')
    # OutputDict(plyy, 'plyy_3DJbmbHtNW1QdonQgWtZYY.csv')
    # plyyToCsv('3DJbmbHtNW1QdonQgWtZYY')