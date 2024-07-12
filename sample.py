import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
 
cid = ''
secret = ''

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager)


result = sp.search('피땀눈물', limit=5, market='KR')
pprint.pprint(result)