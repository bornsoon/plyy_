from spotipy.oauth2 import SpotifyClientCredentials
import spotipy
import pprint

cid = '4a07e98721c84fcab2458d5813965796'
secret = '9fc833bbc4a647c8b56ddb3e952d04b4'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)
sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')

def track(artist, title):
    result = sp.search(title + artist, limit=1)
    rslt = result['tracks']['items'][0]
    albumTitle = rslt['album']['name']
    albumImg = [Img for Img in rslt['album']['images'] if Img['height'] == 640][0]['url']
    artist = rslt['artists'][0]['name']
    srcTitle = rslt['name']
    srcId = rslt['id']

    src = {'Id': srcId, 'Title': srcTitle, 'Artist': artist, 'Album': albumTitle, 'AlbumImg': albumImg}

    return src


def spotify_plyy(playlist_id):
    result = sp.playlist_tracks(playlist_id, additional_types=("track",))

    pprint.pprint(result)
    return result
    

if __name__=='__main__':
    track('케이윌', '체리블라썸')
    spotify_plyy('3axAvtVlnfhenoPSfOel70')