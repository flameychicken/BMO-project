from speech_to_text import recognize_speech
from assistant import get_response
from text_to_speech import speak
from command_executor import execute_command

def main():
    while True:
        try:
            user_input = recognize_speech()
            if not user_input:
                continue

            print(f"🧠 You said: {user_input}")

            if execute_command(user_input):
                speak("Command executed.")
                continue

            reply = get_response(user_input)
            print(f"🤖 AI: {reply}")
            speak(reply)

        except KeyboardInterrupt:
            print("\n👋 Exiting...")
            break
        except Exception as e:
            print(f"❌ Error: {e}")

if __name__ == "__main__":
    main()
