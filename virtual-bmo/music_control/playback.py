import spotipy
from spotipy.oauth2 import SpotifyOAuth
from music_control.spotify_auth import get_token

def get_spotify_client():
    token = get_token()
    return spotipy.Spotify(auth=token)

def play_music():
    sp = get_spotify_client()
    devices = sp.devices()["devices"]
    if not devices:
        print("❌ No active Spotify devices found.")
        return
    device_id = devices[0]["id"]
    sp.start_playback(device_id=device_id)
    print("▶️ BMO started playing music.")

def pause_music():
    sp = get_spotify_client()
    sp.pause_playback()
    print("⏸️ Music paused.")

def next_track():
    sp = get_spotify_client()
    sp.next_track()
    print("⏭️ Skipped to next track.")