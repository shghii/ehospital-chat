import openai
import tempfile
import os
from fastapi import UploadFile

def transcribe_audio(audio_file: UploadFile) -> str:
    try:
        with tempfile.NamedTemporaryFile(delete=False, suffix=".wav") as tmp:
            tmp.write(audio_file.file.read())
            tmp_filename = tmp.name

        transcription = openai.Audio.transcribe("whisper-1", open(tmp_filename, "rb"))
        os.remove(tmp_filename)
        return transcription.get("text", "")
    except Exception as e:
        print("Transcription error:", e)
        return ""
