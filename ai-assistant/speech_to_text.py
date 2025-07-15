import sounddevice as sd
import queue
import vosk
import json
import os

MODEL_PATH = "models/vosk-model"

q = queue.Queue()

def callback(indata, frames, time, status):
    if status:
        print(status)
    q.put(bytes(indata))

def recognize_speech():
    if not os.path.exists(MODEL_PATH):
        raise FileNotFoundError("Vosk model not found.")
    model = vosk.Model(MODEL_PATH)
    samplerate = 16000

    with sd.RawInputStream(samplerate=samplerate, blocksize=8000, dtype='int16',
                           channels=1, callback=callback):
        rec = vosk.KaldiRecognizer(model, samplerate)
        print("🎤 Listening...")
        while True:
            data = q.get()
            if rec.AcceptWaveform(data):
                result = json.loads(rec.Result())
                return result.get("text", "")
