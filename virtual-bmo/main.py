import pygame
import sys
import os
import queue
import sounddevice as sd
import vosk
import pyttsx3
import json

# === Init Pygame ===
pygame.init()
screen = pygame.display.set_mode((480, 320))
pygame.display.set_caption("Virtual BMO")
font = pygame.font.SysFont("Arial", 20)

# === Load BMO image ===
ASSET_PATH = os.path.join("assets", "bmo1.jpg")
try:
    bmo_image = pygame.image.load(ASSET_PATH)
    bmo_image = pygame.transform.scale(bmo_image, (480, 320))
except pygame.error as e:
    print(f"Error loading image: {e}")
    sys.exit(1)

# === TTS setup ===
engine = pyttsx3.init()
def speak(text):
    print(f"BMO: {text}")
    engine.say(text)
    engine.runAndWait()

# === STT setup ===
model_path = os.path.join("voice_ai", "model")
if not os.path.exists(model_path):
    print("❌ Vosk model not found in voice_ai/model/")
    sys.exit(1)

model = vosk.Model(model_path)
q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def listen():
    with sd.RawInputStream(samplerate=16000, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        print("🎤 Listening...")
        rec = vosk.KaldiRecognizer(model, 16000)
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "").lower()

# === Response Logic ===
def respond(command):
    if "music" in command:
        return "Okay! Let's play music."
    elif "game" in command:
        from games.snake_game import run_snake_game
        speak("Launching game mode!")
        run_snake_game()  # Snake game runs, then returns
        return "Hope you enjoyed the game!"
    elif "hello" in command:
        return "Hello friend! I am BMO!"
    elif "bye" in command:
        return "Goodbye! Shutting down."
    else:
        return "I'm not sure what you said."

# === Main Pygame loop ===
current_text = "Press SPACE to talk to BMO"
running = True

while running:
    screen.blit(bmo_image, (0, 0))

    # Render the last voice result
    text_surface = font.render(current_text, True, (0, 0, 0))
    screen.blit(text_surface, (10, 280))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

        # Press SPACE to trigger voice interaction
        if event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
            current_text = "Listening..."
            pygame.display.flip()

            command = listen()
            print("You said:", command)
            response = respond(command)
            speak(response)
            current_text = "BMO: " + response

            if "goodbye" in response.lower():
                running = False

    pygame.display.flip()

pygame.quit()
sys.exit()