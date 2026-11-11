# AI Text Summarization API

A bilingual AI-powered text summarization API developed with Python, FastAPI, PyTorch, and Hugging Face Transformers. The application generates concise summaries from English and French text and supports PDF document summarization.

## Project Overview

This project aims to simplify the process of understanding long documents by using Natural Language Processing (NLP) and transformer-based deep learning models.

Users can submit text or upload PDF documents through a REST API and receive automatically generated summaries in their selected language.

## Features

- English text summarization using DistilBART.
- French text summarization using a French T5 model.
- PDF document text extraction and summarization.
- Long-document processing through text chunking.
- Configurable minimum and maximum summary lengths.
- Input validation using Pydantic.
- REST API with interactive Swagger documentation.
- Model evaluation using ROUGE metrics.
- Automated API testing with pytest.
- Docker containerization.

## Technologies and Tools

| Technology | Purpose |
|---|---|
| Python 3.11 | Main programming language |
| FastAPI | REST API development |
| Uvicorn | ASGI application server |
| PyTorch | Deep learning framework |
| Hugging Face Transformers | Pretrained NLP models |
| DistilBART | English text summarization |
| T5 | French text summarization |
| Pydantic | Request validation and data schemas |
| pypdf | PDF text extraction |
| ROUGE Score | Summarization evaluation |
| pytest | Automated testing |
| Docker | Application containerization |

## AI Models

The project uses two pretrained transformer models:

**English**

- Model: `sshleifer/distilbart-cnn-12-6`
- Architecture: DistilBART
- Purpose: Generate concise English summaries.

**French**

- Model: `xavierbarbier/t5-small-mlsum-fr`
- Architecture: T5
- Purpose: Generate French summaries.

Models are loaded when first required and cached for subsequent requests.

## Project Structure

```text
ai-text-summarization-api/
│
├── app/
│   ├── __init__.py
│   ├── main.py
│   │
│   ├── routes/
│   │   └── __init__.py
│   │
│   ├── schemas/
│   │   ├── __init__.py
│   │   └── summarize.py
│   │
│   └── services/
│       ├── __init__.py
│       ├── summarizer.py
│       └── pdf_reader.py
│
├── reports/
│   ├── phase6_rouge_evaluation.md
│   ├── sample.pdf
│   └── sample_fr.pdf
│
├── tests/
│   ├── evaluate_rouge.py
│   └── test_api.py
│
├── .dockerignore
├── .gitignore
├── Dockerfile
├── requirements.txt
└── README.md
```

## Installation and Setup

### 1. Clone the repository

```bash
git clone <YOUR_REPOSITORY_URL>
cd ai-text-summarization-api
```

### 2. Create a virtual environment

```bash
python3 -m venv venv
```

### 3. Activate the virtual environment

On macOS and Linux:

```bash
source venv/bin/activate
```

### 4. Install dependencies

```bash
pip install -r requirements.txt
```

## Running the API Locally

Start the application using Uvicorn:

```bash
uvicorn app.main:app --reload
```

The API will be available at:

http://127.0.0.1:8000

Interactive Swagger documentation:

http://127.0.0.1:8000/docs

## API Endpoints

| Method | Endpoint | Description |
|---|---|---|
| GET | `/` | Check API availability |
| POST | `/summarize` | Summarize submitted text |
| POST | `/summarize-pdf` | Extract and summarize PDF content |

### 1. Text Summarization

Endpoint:

`POST /summarize`

Example JSON request:

```json
{
  "text": "Artificial intelligence is transforming healthcare, education, and business. It helps professionals analyze information, automate tasks, and make better decisions.",
  "max_length": 100,
  "min_length": 30,
  "language": "en"
}
```

Supported languages:

- `en` — English
- `fr` — French

The API returns the original text and its generated summary.

### 2. PDF Summarization

Endpoint:

`POST /summarize-pdf`

This endpoint accepts a PDF document using multipart form data.

Supported fields:

| Field | Description |
|---|---|
| `file` | PDF document |
| `language` | Summary language: `en` or `fr` |
| `max_length` | Maximum summary length |
| `min_length` | Minimum summary length |

The application extracts readable text from the PDF and passes it to the selected summarization model.

## Long Document Processing

Long documents may exceed the maximum input-token limit of a transformer model.

To handle this, the application implements a chunking strategy:

1. Tokenize the input document.
2. Split long documents into smaller chunks.
3. Generate a summary for each chunk.
4. Combine the individual summaries.
5. Apply a final summarization pass when the combined text fits the model's input limit.

This allows the API to process longer documents while respecting the input limitations of the selected models.

## Model Evaluation

The project uses ROUGE metrics to compare generated summaries with reference summaries.

The evaluation includes:

- ROUGE-1: Measures unigram overlap.
- ROUGE-2: Measures bigram overlap.
- ROUGE-L: Measures the longest common subsequence.

### Average ROUGE F1 Results

| Language | ROUGE-1 | ROUGE-2 | ROUGE-L |
|---|---:|---:|---:|
| English | 0.5318 | 0.2748 | 0.4828 |
| French | 0.4074 | 0.1841 | 0.3306 |

The evaluation dataset contains five documents per language.

These results are preliminary and should not be interpreted as a comprehensive benchmark of either model.

Detailed evaluation results are available in:

`reports/phase6_rouge_evaluation.md`

## Automated Testing

The project includes automated API tests using pytest.

Run the test suite:

```bash
python -m pytest tests/test_api.py -v
```

Current result:

**8 tests passed.**

The tests cover:

- API health check.
- English summarization endpoint.
- French summarization endpoint.
- Short-text validation.
- Invalid-language validation.
- Summary-length validation.
- PDF summarization endpoint.
- Non-PDF file rejection.

The API tests mock the AI summarization and PDF extraction functions to avoid loading large models during the test suite.

## Docker Deployment

The application can be built and executed inside a Docker container.

### 1. Build the Docker image

```bash
docker build -t ai-text-summarization-api .
```

### 2. Run the container

```bash
docker run -d \
  --name ai-summarization-api \
  -p 8000:8000 \
  ai-text-summarization-api
```

### 3. Access the API

Open:

http://localhost:8000/docs

### 4. Stop the container

```bash
docker stop ai-summarization-api
```

The Docker image includes the application and its Python dependencies. Pretrained Hugging Face models are downloaded when required at runtime.

## Current Limitations

- Scanned or image-only PDFs are not supported because OCR has not been implemented.
- French summaries may omit important information in some documents.
- ROUGE evaluation currently uses a small dataset with one reference summary per document.
- The first request may take longer because pretrained models need to be downloaded and loaded.
- Model inference requires sufficient memory.

## Future Improvements

- Implement OCR support for scanned PDF documents.
- Improve French summarization quality.
- Expand the evaluation dataset.
- Add authentication and API rate limiting.
- Improve error handling and logging.
- Deploy the application to a cloud platform.

## Author

Developed as part of a Master's academic project focused on Artificial Intelligence, Natural Language Processing, and Deep Learning.

## License

This project was developed for academic and educational purposes.
