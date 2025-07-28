# summarize.py
from transformers import pipeline

# Load Hugging Face summarizer (model is downloaded on first run)
summarizer = pipeline("summarization", model="facebook/bart-large-cnn")

def summarize_with_huggingface(text: str) -> str:
    """
    Summarize using free Hugging Face BART model.
    """
    # HF models may fail with too long input, truncate manually if needed
    max_input_length = 1024
    text = text[:max_input_length]

    summary = summarizer(text, max_length=150, min_length=40, do_sample=False)
    return summary[0]["summary_text"]


# Placeholder: To use OpenAI GPT instead
# Requires: pip install openai and OPENAI_API_KEY in env

# def summarize_with_openai(text: str) -> str:
#     import openai
#     openai.api_key = os.getenv("OPENAI_API_KEY")
#     response = openai.ChatCompletion.create(
#         model="gpt-4",
#         messages=[{"role": "user", "content": f"Summarize this:\n{text}"}],
#         temperature=0.3
#     )
#     return response.choices[0].message["content"]

# Placeholder: Vertex AI Gemini upgrade
# Requires: pip install google-cloud-aiplatform and credentials
# from vertexai.preview.generative_models import GenerativeModel
# model = GenerativeModel("gemini-1.5-flash-preview")
# response = model.generate_content([f"Summarize this:\n{text}"])
# return response.text
