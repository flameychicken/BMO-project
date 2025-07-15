# tools/actions.py
from datetime import datetime

def handle_tool(command):
    if "time" in command:
        now = datetime.now().strftime("%I:%M %p")
        return f"The time is {now}."
    elif "game" in command:
        return "Let's play a game! (feature launching soon)"
    else:
        return None
