# utils/translator.py
from transformers import pipeline

MODEL_MAP = {
    "Hindi": "Helsinki-NLP/opus-mt-en-hi",
    "French": "Helsinki-NLP/opus-mt-en-fr",
    "Spanish": "Helsinki-NLP/opus-mt-en-es",
    "German": "Helsinki-NLP/opus-mt-en-de",
    "Telugu": "ai4bharat/indictrans2-en-te"
}

translator_pipelines = {}

def get_pipeline_for_language(lang):
    model_name = MODEL_MAP.get(lang)
    if not model_name:
        raise ValueError(f"No model available for {lang}")
    if model_name not in translator_pipelines:
        translator_pipelines[model_name] = pipeline("translation", model=model_name)
    return translator_pipelines[model_name]

def translate_text(text, lang, chunk_size=400):
    translator = get_pipeline_for_language(lang)

    # Break text into chunks
    chunks = [text[i:i+chunk_size] for i in range(0, len(text), chunk_size)]
    translated_chunks = []

    for chunk in chunks:
        try:
            translated = translator(chunk, max_length=512)[0]["translation_text"]
            translated_chunks.append(translated)
        except Exception as e:
            translated_chunks.append(f"[Error translating chunk: {e}]")
    
    return "\n".join(translated_chunks)