import os
import pytesseract

# Configure Tesseract path if needed
pytesseract.pytesseract.tesseract_cmd = os.getenv(
    'TESSERACT_PATH',
    '/usr/bin/tesseract'  # Default Linux path
)
