
import os
import tempfile

from fastapi import FastAPI, HTTPException, UploadFile, File, Form

from app.schemas.summarize import SummarizeRequest, SummarizeResponse
from app.services.summarizer import summarize_text
from app.services.pdf_reader import extract_text_from_pdf


# Initialize FastAPI application
app = FastAPI(
    title="AI Text Summarization API",
    description="""
    ## AI-powered Text Summarization

    This API uses Natural Language Processing (NLP)
    and Transformer models to summarize text in English and French.

    ### Features

    - Summarize short and long documents.
    - Support English (DistilBART) and French (T5).
    - Customize summary length.
    - Automatically process long texts using chunking.
    - Extract text from PDF documents.
    - Validate input parameters.
    - Return structured JSON responses.
    """,
    version="1.0.0"
)


# Root endpoint
@app.get(
    "/",
    tags=["General"],
    summary="Check API status"
)
def home():
    return {
        "message": "Welcome to the AI Text Summarization API!",
        "status": "API is running"
    }


# Text summarization endpoint
@app.post(
    "/summarize",
    response_model=SummarizeResponse,
    tags=["Summarization"],
    summary="Summarize text"
)
def create_summary(request: SummarizeRequest):
    try:
        summary = summarize_text(
            text=request.text,
            max_length=request.max_length,
            min_length=request.min_length,
            language=request.language
        )

        if not summary:
            raise HTTPException(
                status_code=500,
                detail="The summarization model could not generate a summary."
            )

        return SummarizeResponse(
            original_text=request.text,
            summary=summary
        )

    except HTTPException:
        raise

    except Exception as exc:
        print(f"TEXT SUMMARIZATION ERROR: {exc!r}", flush=True)
        import traceback
        traceback.print_exc()
        raise HTTPException(
        status_code=500,
        detail="An unexpected error occurred while generating the summary."
    )


# PDF summarization endpoint
@app.post(
    "/summarize-pdf",
    response_model=SummarizeResponse,
    tags=["PDF Summarization"],
    summary="Summarize a PDF document"
)
async def summarize_pdf(
    file: UploadFile = File(..., description="PDF document to summarize"),
    language: str = Form("en", description="Summary language: en or fr"),
    max_length: int = Form(130, ge=30, le=250),
    min_length: int = Form(30, ge=10, le=100)
):
    temp_path = None

    try:
        # Validate file
        if not file.filename or not file.filename.lower().endswith(".pdf"):
            raise HTTPException(
                status_code=400,
                detail="Please upload a PDF file."
            )

        if language.lower().strip() not in ["en", "fr"]:
            raise HTTPException(
                status_code=422,
                detail="Language must be 'en' or 'fr'."
            )

        if min_length >= max_length:
            raise HTTPException(
                status_code=422,
                detail="min_length must be smaller than max_length."
            )

        # Read uploaded PDF
        content = await file.read()

        if not content:
            raise HTTPException(
                status_code=400,
                detail="The uploaded PDF is empty."
            )

        # Save temporarily
        with tempfile.NamedTemporaryFile(
            suffix=".pdf",
            delete=False
        ) as temp_file:
            temp_file.write(content)
            temp_path = temp_file.name

        # Extract PDF text
        extracted_text = extract_text_from_pdf(temp_path)

        if len(extracted_text) < 50:
            raise HTTPException(
                status_code=422,
                detail="The PDF must contain at least 50 readable characters."
            )

        # Generate summary
        summary = summarize_text(
            text=extracted_text,
            max_length=max_length,
            min_length=min_length,
            language=language.lower().strip()
        )

        if not summary:
            raise HTTPException(
                status_code=500,
                detail="The summarization model could not generate a summary."
            )

        return SummarizeResponse(
            original_text=extracted_text,
            summary=summary
        )

    except HTTPException:
        raise

    except ValueError as exc:
        raise HTTPException(
            status_code=422,
            detail=str(exc)
        )

    except Exception:
        raise HTTPException(
            status_code=500,
            detail="An unexpected error occurred while processing the PDF."
        )

    finally:
        # Remove temporary PDF file
        if temp_path and os.path.exists(temp_path):
            os.remove(temp_path)

        await file.close()
