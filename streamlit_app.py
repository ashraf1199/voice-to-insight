import streamlit as st
import os
import numpy as np
from transcribe import transcribe_audio
from summarize import summarize_with_huggingface
from st_audiorec import st_audiorec

# Setup
st.set_page_config(page_title="🎙️ Voice-to-Insight", layout="centered")
st.title("🎙️ Voice-to-Insight: Real-Time Meeting Summarizer")

UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

input_mode = st.radio("Choose your input method:", ["Upload Audio File", "Record from Microphone"])
audio_path = None

# ===== Upload Section =====
if input_mode == "Upload Audio File":
    uploaded_file = st.file_uploader("Upload a .wav, .mp3, or .m4a audio file", type=["wav", "mp3", "m4a"])
    if uploaded_file:
        audio_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(audio_path, "wb") as f:
            f.write(uploaded_file.read())
        st.audio(audio_path)
        st.success("✅ Audio file uploaded successfully!")

# ===== Microphone Section =====
elif input_mode == "Record from Microphone":
    st.info("🎙️ Click to record audio below")

    wav_audio_data = st_audiorec()

    if wav_audio_data is not None:
        audio_path = os.path.join(UPLOAD_DIR, "mic_recorded.wav")
        with open(audio_path, "wb") as f:
            f.write(wav_audio_data)

        st.audio(audio_path)
        st.success("✅ Microphone recording saved successfully!")

# ===== Transcription & Summarization =====
if audio_path and os.path.exists(audio_path):
    if st.button("🔍 Transcribe & Summarize"):
        st.info(f"Processing file: `{os.path.basename(audio_path)}`")

        with st.spinner("🔡 Transcribing..."):
            try:
                transcript = transcribe_audio(audio_path)
                st.subheader("📝 Transcript")
                st.write(transcript if transcript.strip() else "❗ No transcription found.")
            except Exception as e:
                st.error(f"Transcription Error: {str(e)}")
                transcript = None

        if transcript:
            with st.spinner("📌 Summarizing..."):
                try:
                    summary = summarize_with_huggingface(transcript)
                    st.subheader("📌 Summary")
                    st.write(summary if summary.strip() else "❗ No summary generated.")
                except Exception as e:
                    st.error(f"Summarization Error: {str(e)}")
        else:
            st.warning("🛑 Skipping summarization due to transcription failure.")

else:
    st.info("Please upload or record audio to get started.")
