import os
from dotenv import load_dotenv
import qrcode
import webbrowser
import threading
from flask import Flask, request
from spotipy.oauth2 import SpotifyOAuth

load_dotenv()  # loads the .env file

client_id = os.getenv('SPOTIPY_CLIENT_ID')
client_secret = os.getenv('SPOTIPY_CLIENT_SECRET')
redirect_uri = os.getenv('SPOTIPY_REDIRECT_URI')

auth_token = None
app = Flask(__name__)

def start_server():
    app.run(port=8888)

@app.route("/callback")
def callback():
    global auth_token
    code = request.args.get("code")
    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        client_secret=client_secret,
        redirect_uri=redirect_uri,
        scope="user-read-playback-state,user-modify-playback-state"
    )
    token_info = sp_oauth.get_access_token(code)
    auth_token = token_info["access_token"]
    return "✅ BMO connected to Spotify! You can close this tab."

def get_token():
    global auth_token
    if auth_token:
        return auth_token

    sp_oauth = SpotifyOAuth(
        client_id=client_id,
        redirect_uri=redirect_uri,
        scope="user-read-playback-state user-modify-playback-state",
        open_browser=False,
    )
    auth_url = sp_oauth.get_authorize_url()

    img = qrcode.make(auth_url)
    img.save("assets/spotify_qr.png")
    print("📲 Scan QR from assets/spotify_qr.png to connect Spotify")

    # Also open in browser for convenience
    webbrowser.open(auth_url)

    threading.Thread(target=start_server).start()

    print("🔃 Waiting for Spotify login...")
    while not auth_token:
        pass

    return auth_token