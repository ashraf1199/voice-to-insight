# transcribe.py
import whisper
import torch
import os

def transcribe_audio(audio_path: str) -> str:
    if not os.path.exists(audio_path):
        raise FileNotFoundError(f"Audio file not found: {audio_path}")

    # Automatically choose GPU if available, else CPU
    device = "cuda" if torch.cuda.is_available() else "cpu"

    print(f"🔍 Using device: {device}")

    model = whisper.load_model("base", device=device)
    result = model.transcribe(audio_path)

    return result["text"]
