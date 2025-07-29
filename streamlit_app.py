import streamlit as st
import os
import numpy as np
import wave
from transcribe import transcribe_audio
from summarize import summarize_with_huggingface
from streamlit_webrtc import webrtc_streamer, AudioProcessorBase
import av
import uuid

st.set_page_config(page_title="🎙️ Voice-to-Insight", layout="centered")
st.title("🎙️ Voice-to-Insight: Real-Time Meeting Summarizer")

# Directory to store audio
UPLOAD_DIR = "uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)

# Input mode selector
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
    class AudioProcessor(AudioProcessorBase):
        def __init__(self):
            self.frames = []

        def recv(self, frame: av.AudioFrame) -> av.AudioFrame:
            data = frame.to_ndarray()
            self.frames.append(data)
            return frame
    unique_key = str(uuid.uuid4())
    ctx = webrtc_streamer(
        key=unique_key,
        mode="sendonly",
        audio_receiver_size=1024,
        media_stream_constraints={"audio": True, "video": False},
        rtc_configuration={"iceServers": [{"urls": ["stun:stun.l.google.com:19302"]}]},
        async_processing=True,
    )

    if ctx.audio_receiver:
        st.warning("🎙️ Recording... press the 'Stop' button above when you're done.")
        if st.button("Save Recording"):
            audio_processor = ctx.audio_processor
            if not audio_processor or not audio_processor.frames:
                st.error("No audio frames recorded.")
            else:
                audio_data = np.concatenate(audio_processor.frames, axis=1).flatten().astype(np.int16)
                audio_path = os.path.join(UPLOAD_DIR, "mic_recording.wav")
                with wave.open(audio_path, "wb") as wf:
                    wf.setnchannels(1)
                    wf.setsampwidth(2)
                    wf.setframerate(48000)
                    wf.writeframes(audio_data.tobytes())
                st.audio(audio_path)
                st.success("✅ Recording saved successfully!")

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
