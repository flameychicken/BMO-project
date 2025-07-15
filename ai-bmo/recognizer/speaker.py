import subprocess
import os

def speak(text):
    """
    Text-to-speech function that works on Windows without pywin32.
    Tries multiple methods from pyttsx3 engines to PowerShell and VBScript.
    """
    try:
        import pyttsx3
        try:
            engine = pyttsx3.init('espeak')
            engine.say(text)
            engine.runAndWait()
            return
        except Exception:
            try:
                engine = pyttsx3.init()
                engine.say(text)
                engine.runAndWait()
                return
            except Exception:
                pass
    except ImportError:
        pass

    try:
        escaped_text = text.replace('"', '""').replace('\n', ' ')
        powershell_cmd = f'Add-Type -AssemblyName System.Speech; $speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; $speak.Speak("{escaped_text}")'
        subprocess.run(['powershell', '-Command', powershell_cmd], check=True, capture_output=True)
        return
    except subprocess.CalledProcessError:
        pass

    try:
        escaped_text = text.replace('"', '""').replace('\n', ' ')
        vbs_script = f'''
Dim speaks, speech
speaks = "{escaped_text}"
Set speech = CreateObject("sapi.spvoice")
speech.Speak speaks
'''
        temp_file = "temp_speech.vbs"
        with open(temp_file, "w", encoding="utf-8") as f:
            f.write(vbs_script)

        subprocess.run(["cscript", "//nologo", temp_file], check=True)
        os.remove(temp_file)
        return
    except Exception:
        if os.path.exists(temp_file):
            os.remove(temp_file)

    print(f"🔊 SPEECH: {text}")
