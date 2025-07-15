import warnings
import torch
from transformers import pipeline, set_seed
from recognizer.recognizer import listen_for_command

# Suppress unnecessary warnings
warnings.filterwarnings("ignore")

# Load a better small chat-capable model
chatbot = pipeline("text-generation", model="tiiuae/falcon-rw-1b", device=0 if torch.cuda.is_available() else -1)

# Optional: Set seed for consistent output
set_seed(42)

def main():
    print("🎤 Listening for command...")
    command = listen_for_command()
    if command:
        print(f"🗣️  You said: {command}")
        response = chatbot(command, max_length=100, truncation=True)[0]['generated_text']
        # Strip the input prompt from the generated output
        clean_response = response.replace(command, "").strip()
        print(f"🤖 AI: {clean_response}")

if __name__ == "__main__":
    main()
