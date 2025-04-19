# This stub uses whisper.cpp CLI; replace with streaming logic later.
import subprocess
import tempfile
import os

WHISPER_CPP_PATH = "./whisper.cpp/main"  # adjust to your whisper.cpp binary
MODEL_PATH = "./models/tiny.en.gguf"     # adjust to your Whisper model file

def transcribe() -> str:
    # record to a temp WAV, run whisper, then delete
    with tempfile.NamedTemporaryFile(suffix=".wav", delete=False) as tf:
        wav_path = tf.name
    try:
        # Use whatever recording tool you prefer (this is just placeholder)
        # e.g., `arecord` on Linux or `sox` cross‑platform
        # subprocess.run(["record-audio", wav_path, "--duration", "10"], check=True)
        cmd = [
            WHISPER_CPP_PATH,
            "-m", MODEL_PATH,
            "-f", wav_path,
            "--stream"  # hypothetical real-time flag
        ]
        result = subprocess.run(cmd, stdout=subprocess.PIPE, stderr=subprocess.PIPE, check=True, text=True)
        return result.stdout.strip()
    finally:
        try:
            os.remove(wav_path)
        except OSError:
            pass
