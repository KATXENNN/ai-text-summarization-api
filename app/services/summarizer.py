
import re
import torch

from transformers import AutoTokenizer, AutoModelForSeq2SeqLM


# Model configuration
MODELS = {
    "en": {
        "name": "sshleifer/distilbart-cnn-12-6",
        "max_input_tokens": 1024,
        "chunk_size": 900,
        "prefix": ""
    },
    "fr": {
        "name": "xavierbarbier/t5-small-mlsum-fr",
        "max_input_tokens": 512,
        "chunk_size": 450,
        "prefix": "summarize: "
    }
}


# Select Apple GPU when available
DEVICE = torch.device(
    "mps" if torch.backends.mps.is_available() else "cpu"
)

print(f"Summarization device: {DEVICE}")


# Cache models after their first use
MODEL_CACHE = {}


# Load a model when needed
def load_model(language: str):
    """Load and cache the requested language model."""

    if language not in MODELS:
        raise ValueError("Language must be 'en' or 'fr'.")

    if language not in MODEL_CACHE:
        model_name = MODELS[language]["name"]

        print(f"Loading {language.upper()} model: {model_name}")

        tokenizer = AutoTokenizer.from_pretrained(model_name)

        model = AutoModelForSeq2SeqLM.from_pretrained(model_name)

        model.to(DEVICE)
        model.eval()

        MODEL_CACHE[language] = {
            "tokenizer": tokenizer,
            "model": model
        }

        print(f"{language.upper()} model loaded successfully!")

    return MODEL_CACHE[language]["tokenizer"], MODEL_CACHE[language]["model"]


# Clean input text
def clean_text(text: str) -> str:
    """Clean unnecessary spaces and line breaks."""

    text = re.sub(r"\s+", " ", text)
    text = re.sub(r"\s+([.,!?;:])", r"\1", text)

    return text.strip()


# Summarize one chunk
def summarize_chunk(
    text: str,
    tokenizer,
    model,
    language: str,
    max_length: int = 130,
    min_length: int = 30
) -> str:
    """Generate a summary for one text chunk."""

    prefix = MODELS[language]["prefix"]

    inputs = tokenizer(
        prefix + text,
        return_tensors="pt",
        truncation=True,
        max_length=MODELS[language]["max_input_tokens"]
    )

    inputs = {
        key: value.to(DEVICE)
        for key, value in inputs.items()
    }

    with torch.inference_mode():
        summary_ids = model.generate(
            **inputs,
            max_length=max_length,
            min_length=min_length,
            do_sample=False
        )

    return tokenizer.decode(
        summary_ids[0],
        skip_special_tokens=True
    )


# Summarize complete text, including long documents
def summarize_text(
    text: str,
    max_length: int = 130,
    min_length: int = 30,
    language: str = "en"
) -> str:
    """Summarize short and long documents in English or French."""

    language = language.lower().strip()

    if language not in MODELS:
        raise ValueError("Language must be 'en' or 'fr'.")

    # Load the requested language model
    tokenizer, model = load_model(language)

    # Clean input text
    text = clean_text(text)

    # Get model-specific token limits
    max_input_tokens = MODELS[language]["max_input_tokens"]
    chunk_size = MODELS[language]["chunk_size"]

    # Convert text into tokens
    token_ids = tokenizer(
        text,
        add_special_tokens=False,
        verbose=False
    )["input_ids"]

    # Short documents: summarize directly
    if len(token_ids) <= max_input_tokens:
        return clean_text(
            summarize_chunk(
                text,
                tokenizer,
                model,
                language,
                max_length,
                min_length
            )
        )

    # Long documents: split into smaller chunks
    chunks = []

    for i in range(0, len(token_ids), chunk_size):
        chunk_ids = token_ids[i:i + chunk_size]

        chunk_text = tokenizer.decode(
            chunk_ids,
            skip_special_tokens=True
        )

        if chunk_text.strip():
            chunks.append(chunk_text)

    # Summarize each chunk
    summaries = []

    for index, chunk in enumerate(chunks, start=1):
        print(f"Summarizing {language.upper()} chunk {index}/{len(chunks)}...")

        summary = summarize_chunk(
            chunk,
            tokenizer,
            model,
            language,
            max_length,
            min_length
        )

        summaries.append(clean_text(summary))

    # Combine individual summaries
    combined_summary = clean_text(" ".join(summaries))

    # Tokenize combined summaries
    combined_tokens = tokenizer(
        combined_summary,
        add_special_tokens=False,
        verbose=False
    )["input_ids"]

    # Apply a second summarization pass when possible
    if len(combined_tokens) <= max_input_tokens:
        print("Applying final summarization pass...")

        final_summary = summarize_chunk(
            combined_summary,
            tokenizer,
            model,
            language,
            max_length,
            min_length
        )

        return clean_text(final_summary)

    # Return combined summaries if they exceed model capacity
    return combined_summary
