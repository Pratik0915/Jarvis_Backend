from fastapi import APIRouter, UploadFile, File
from .pdf import extract_pdf_text
from .pdf_memory import save_pdf_text, get_pdf_text


router = APIRouter()


@router.post("/upload-pdf")
async def upload_pdf(file: UploadFile = File(...)):

    text = extract_pdf_text(file.file)

    save_pdf_text(text)

    return {
        "message": "PDF uploaded successfully!",
        "characters": len(text)
    }


@router.get("/pdf-text")
def pdf_text():

    text = get_pdf_text()

    return {
        "text": text
    }