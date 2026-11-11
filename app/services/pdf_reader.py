
from pypdf import PdfReader


def extract_text_from_pdf(file_path: str) -> str:
    """Extract readable text from a PDF file."""
    try:
        reader = PdfReader(file_path)

        pages_text = []

        for page in reader.pages:
            page_text = page.extract_text() or ""
            if page_text.strip():
                pages_text.append(page_text)

        extracted_text = "\n".join(pages_text).strip()

        if not extracted_text:
            raise ValueError(
                "No readable text found. The PDF may contain scanned images."
            )

        return extracted_text

    except Exception as exc:
        raise ValueError(f"Unable to read PDF: {exc}") from exc
