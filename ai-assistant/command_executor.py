import os

def execute_command(text: str) -> bool:
    text = text.lower()
    if "open notepad" in text:
        os.system("start notepad")
        return True
    elif "open calculator" in text:
        os.system("start calc")
        return True
    return False
