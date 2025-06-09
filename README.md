# BMO-project

To get started with a Virtual Environment :

1. cd into virtual-bmo
2. create a virtual environment
- python3 -m venv
3. activate virtual environment
- source venv/bin/activate
4. install requirements
- pip install -r requirements.txt

### 🛠️ Tools & Technologies Used

| Feature                        | Tool / Library | Purpose |
|-------------------------------|----------------|---------|
| **UI + Animation**            | `pygame` | Handles BMO’s face, screen output, and in-game visuals |
| **Voice Input (STT)**         | `vosk` | Offline speech-to-text for understanding commands |
| **Microphone Access**         | `sounddevice` | Captures real-time audio from your microphone |
| **Voice Output (TTS)**        | `pyttsx3` + `espeak` | Offline text-to-speech engine for BMO's voice |
| **AI Logic (Local)**          | Python (rule-based) | Logic that maps speech to commands like “play music” |
| **Music Integration**         | `spotipy` | Controls Spotify playback through the Web API |
| **QR Code Generator**         | `qrcode` | Displays Spotify login links as QR codes |
| **Web Server**                | `flask` | Receives Spotify authorization callback |
| **Game Engine**               | `pygame` | Runs retro-style games like Snake |
| **Spotify API**               | [Spotify Developer Platform](https://developer.spotify.com) | Enables user login and music control (free tier) |
| **Image Rendering**           | `pygame.image.load()` | Displays BMO face and dynamic QR codes |
| **Environment Management**    | `venv`, `.gitignore` | Manages dependencies and ignores clutter in Git |

_All tools above are open-source or free to use with a developer account._