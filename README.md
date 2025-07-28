# 🎙️ Voice-to-Insight: Real-Time Meeting Summarizer

An AI-powered Streamlit web app that:
- Transcribes spoken meetings in real-time using OpenAI Whisper
- Summarizes key points using Hugging Face Transformers
- Accepts both audio file upload or live microphone input
- Runs locally or on [Streamlit Cloud](https://streamlit.io/cloud) for free

---

## 🧰 Features

- 🎤 Microphone or file-based input
- 📄 Whisper transcription (GPU/CPU auto-detect)
- ✨ Summarization via `facebook/bart-large-cnn`
- ☁️ Ready for deployment on Streamlit Cloud

---

## 🚀 Getting Started

### 🔧 Prerequisites

- Python 3.8 or newer
- `ffmpeg` installed locally (Mac/Linux: `brew install ffmpeg`)

### 🖥️ Local Setup

```bash
git clone https://github.com/yourusername/voice-to-insight.git
cd voice-to-insight

python3 -m venv venv
source venv/bin/activate

pip install -r requirements.txt
streamlit run streamlit_app.py


You can easily upgrade this app for more powerful summarization capabilities:

🧠 OpenAI GPT (e.g., GPT-4)
Use OpenAI’s state-of-the-art summarization via ChatCompletion API
Delivers more contextual and accurate summaries for complex transcripts
Requires: openai package + API key
☁️ Google Vertex AI (Gemini 1.5 Flash)
Integrate with Google Cloud’s Gemini models for enterprise-grade performance
Useful for apps running in GCP or requiring scalable inference
Requires: google-cloud-aiplatform + GCP setup
📦 How to Upgrade
Swap the summarization function in summarize.py
Choose based on your available resources and desired performance
Details and code examples are provided in code comments for easy switch