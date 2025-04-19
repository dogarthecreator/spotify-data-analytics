import os
import spotipy
from spotipy.oauth2 import SpotifyOAuth
from flask import Flask, request, redirect, session, url_for
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

app = Flask(__name__)

# Set up the Flask session to store the authorization tokens
app.secret_key = os.urandom(24)
app.config['SESSION_COOKIE_NAME'] = 'spotify-auth'

# Spotify API credentials from the .env file
CLIENT_ID = os.getenv('SPOTIPY_CLIENT_ID')
CLIENT_SECRET = os.getenv('SPOTIPY_CLIENT_SECRET')
REDIRECT_URI = os.getenv('SPOTIPY_REDIRECT_URI')

# Set up Spotify OAuth
sp_oauth = SpotifyOAuth(client_id=CLIENT_ID,
                         client_secret=CLIENT_SECRET,
                         redirect_uri=REDIRECT_URI,
                         scope="user-library-read user-top-read")

@app.route('/')
def index():
    if not session.get("token_info"):
        return redirect(url_for("login"))
    sp = spotipy.Spotify(auth=session.get("token_info")["access_token"])
    results = sp.current_user()
    return f'Hello, {results["display_name"]}'

@app.route('/login')
def login():
    auth_url = sp_oauth.get_authorize_url()
    return redirect(auth_url)

@app.route('/callback')
def callback():
    token_info = sp_oauth.get_access_token(request.args['code'])
    session['token_info'] = token_info
    return redirect(url_for("index"))

if __name__ == "__main__":
    app.run(debug=True, port=8888)
