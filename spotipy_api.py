from spotipy.oauth2 import SpotifyClientCredentials
import spotipy

cid = '4a07e98721c84fcab2458d5813965796'
secret = '9fc833bbc4a647c8b56ddb3e952d04b4'
client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

def song_sample(title, artist):

    sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')

    result = sp.search(title + artist, limit=1, market='KR')

    song = {}

    return 