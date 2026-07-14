from app.pdf import extract_pdf_text

with open("test.pdf", "rb") as file:
    text = extract_pdf_text(file)

print(text)