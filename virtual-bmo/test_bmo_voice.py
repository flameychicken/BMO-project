import pyttsx3

engine = pyttsx3.init()

# List available voices
voices = engine.getProperty('voices')
print("Available voices:\n")
for i, voice in enumerate(voices):
    print(f"{i}: {voice.name} - {voice.id}")

# Choose a voice (you can change the index)
engine.setProperty('voice', voices[2].id)  # Change index after testing voices

# Modify speech rate (words per minute)
engine.setProperty('rate', 200)  # 150–200 is good for cartoony sound

# Speak something
engine.say("Hello, I am BMO! Let's go on an adventure.")
engine.say("This is a test of my new voice. Isn't it cute?")
engine.runAndWait()
