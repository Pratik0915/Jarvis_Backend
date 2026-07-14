from pypdf import PdfReader


def extract_pdf_text(file) -> str:
    """
    Extract text from an uploaded PDF file.
    """

    try:
        reader = PdfReader(file)

        text = ""

        for page in reader.pages:
            page_text = page.extract_text()

            if page_text:
                text += page_text + "\n"

        return text.strip()

    except Exception as e:
        raise Exception(f"Failed to read PDF: {str(e)}")