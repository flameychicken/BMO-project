import subprocess
import os

def speak(text: str):
    print(f"🗣️ Speaking: {text}")
    output_path = "output.wav"

    if os.path.exists(output_path):
        os.remove(output_path)

    # Absolute path to piper.exe
    piper_path = os.path.abspath(os.path.join("piper", "piper.exe"))
    model_path = os.path.abspath(os.path.join("models", "en_US-lessac-medium.onnx"))

    # Run Piper without shell=True, and pass text via stdin
    process = subprocess.Popen(
        [piper_path, "--model", model_path, "--output_file", output_path],
        stdin=subprocess.PIPE,
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE,
        text=True  # handles encoding/decoding automatically
    )

    stdout, stderr = process.communicate(input=text)

    if process.returncode != 0:
        print("❌ Piper failed.")
        print(stderr)
        return

    # Use 'start' to play wav in PowerShell with shell=True
    subprocess.run(["start", output_path], shell=True)
