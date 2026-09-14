import pytesseract


def extract_text(image_path: str, language: str = "eng") -> str:
    """Extract text from an image with Tesseract."""
    text = pytesseract.image_to_string(image_path, lang=language)
    return text.strip()
