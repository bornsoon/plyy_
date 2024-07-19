import spotipy
from spotipy.oauth2 import SpotifyClientCredentials
import pprint
from dotenv import load_dotenv
import os

load_dotenv()

OWM_API_KEY = os.getenv('OPENWEATHERMAP_API_KEY')

cid = os.getenv('SPOTIFY_CID')
secret = os.getenv('SPOTIFY_SECRET')

client_credentials_manager = SpotifyClientCredentials(client_id=cid, client_secret=secret)

sp = spotipy.Spotify(client_credentials_manager=client_credentials_manager, language='ko')


result = sp.search('케이윌 love blossom', limit=1, market='KR')
result = sp.search('로꼬 say yes', limit=1, market='KR')
pprint.pprint(result)