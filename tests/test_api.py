import importlib

from fastapi.testclient import TestClient

main_module = importlib.import_module("app.main")
client = TestClient(main_module.app)

SAMPLE_TEXT = (
    "Artificial intelligence is transforming healthcare and education. "
    "It helps professionals analyze information, automate tasks, "
    "and make better decisions using modern technology."
)

SAMPLE_SUMMARY = "Artificial intelligence helps professionals improve decisions."


def mock_summarize_text(text, max_length=130, min_length=30, language="en"):
    return SAMPLE_SUMMARY


def test_home():
    response = client.get("/")

    assert response.status_code == 200
    assert response.json()["status"] == "API is running"


def test_summarize_english(monkeypatch):
    monkeypatch.setattr(main_module, "summarize_text", mock_summarize_text)

    response = client.post("/summarize", json={
        "text": SAMPLE_TEXT,
        "language": "en"
    })

    assert response.status_code == 200
    assert response.json()["summary"] == SAMPLE_SUMMARY
    assert response.json()["original_text"] == SAMPLE_TEXT


def test_summarize_french(monkeypatch):
    monkeypatch.setattr(main_module, "summarize_text", mock_summarize_text)

    response = client.post("/summarize", json={
        "text": SAMPLE_TEXT,
        "language": "fr"
    })

    assert response.status_code == 200
    assert response.json()["summary"] == SAMPLE_SUMMARY


def test_reject_short_text():
    response = client.post("/summarize", json={
        "text": "Too short",
        "language": "en"
    })

    assert response.status_code == 422


def test_reject_invalid_language():
    response = client.post("/summarize", json={
        "text": SAMPLE_TEXT,
        "language": "es"
    })

    assert response.status_code == 422


def test_reject_invalid_summary_lengths():
    response = client.post("/summarize", json={
        "text": SAMPLE_TEXT,
        "min_length": 100,
        "max_length": 80
    })

    assert response.status_code == 422


def test_summarize_pdf(monkeypatch):
    monkeypatch.setattr(
        main_module,
        "extract_text_from_pdf",
        lambda file_path: SAMPLE_TEXT
    )
    monkeypatch.setattr(main_module, "summarize_text", mock_summarize_text)

    response = client.post(
        "/summarize-pdf",
        files={"file": ("sample.pdf", b"fake PDF content", "application/pdf")},
        data={"language": "en"}
    )

    assert response.status_code == 200
    assert response.json()["original_text"] == SAMPLE_TEXT
    assert response.json()["summary"] == SAMPLE_SUMMARY


def test_reject_non_pdf_file():
    response = client.post(
        "/summarize-pdf",
        files={"file": ("sample.txt", b"Some text", "text/plain")}
    )

    assert response.status_code == 400
    assert response.json()["detail"] == "Please upload a PDF file."
