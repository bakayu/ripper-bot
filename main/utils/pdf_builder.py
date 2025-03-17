from fpdf import FPDF
import pyphen
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime
from PIL import Image, ImageOps
import pytesseract
import asyncio
import io

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')


class GeminiFormatter:
    def format_text(self, text: str) -> str:
        """Use Gemini for text formatting and refinement"""
        response = model.generate_content(f"""
        Format this text into clean paragraphs with proper line breaks and punctuation.
        Preserve all original content:
        
        {text}
        """)
        return response.text


class NoMetaPDF(FPDF):
    def __init__(self):
        super().__init__()
        # Clear standard metadata fields
        self.set_title("")
        self.set_author("")
        self.set_creator("")
        self.set_producer("")
        self.set_subject("")
        self.set_lang("")
        self.set_keywords("")
        self.set_creation_date(datetime(2000, 1, 1, 0, 0))

        self.add_font('NotoSans', '',
                      '/usr/share/fonts/noto/NotoSans-Regular.ttf', uni=True)
        self.set_font('NotoSans', size=11)
        self.set_margins(20, 15, 20)
        self.set_auto_page_break(True, margin=15)

    def _put_info(self):
        """Override to completely disable metadata generation"""
        pass


def create_pdf(text_contents, output_path):
    """Create PDF using Gemini-formatted text"""
    formatter = GeminiFormatter()
    # print(text_contents)
    formatted_text = formatter.format_text("\n".join(text_contents))

    pdf = NoMetaPDF()
    pdf.add_page()

    # Increase page width margins
    pdf.set_margins(20, 15, 20)
    pdf.set_auto_page_break(True, margin=15)

    for paragraph in formatted_text.split('\n\n'):
        if paragraph.strip():
            # print(paragraph, '\n')
            # Set alignment based on content length
            pdf.set_font('NotoSans', size=11)  # Slightly reduce font size

            # Handle long words by using justified alignment
            pdf.set_font_size(11)
            pdf.set_x(20)  # Reset x position
            pdf.multi_cell(0, 6, paragraph.strip(), align='J',
                           border=0, markdown=False)
            pdf.ln(4)

    pdf.output(output_path)
    return formatted_text


async def process_single_image(image_data):
    """Enhanced OCR processing with AI components"""
    try:
        image = Image.open(io.BytesIO(image_data))

        # Check image width and downscale if too wide
        # (preserve height for long screenshots)
        max_width = 1800  # Maximum width in pixels
        if image.width > max_width:
            # Calculate new size while maintaining aspect ratio
            new_width = max_width
            new_height = int(image.height * (max_width / image.width))

            # Resize using high-quality downsampling
            image = image.resize((new_width, new_height), Image.LANCZOS)

        # Preprocess image
        image = image.convert('L')  # Convert to grayscale
        image = ImageOps.autocontrast(image)  # Improve contrast

        custom_config = r'''
            --oem 3 --psm 11
            -c preserve_interword_spaces=1 
            textord_space_size_is_variable=1 
            textord_min_space_size=20  # Minimum pixel gap between words
            textord_heavy_nr=1  # Aggressive noise removal
            thresholding_method=2  # Automatic adaptive threshold
            tessedit_write_params_to_file=
        '''

        text = await asyncio.to_thread(
            pytesseract.image_to_string,
            image,
            lang='eng',
            config=custom_config
        )

        return post_process_text(text)

    except Exception as e:
        raise OCRProcessingError(f"OCR failed: {str(e)}")


def post_process_text(text):
    """Clean up OCR output text"""
    # Basic text cleanup
    text = text.strip()
    # Remove multiple consecutive whitespaces
    import re
    text = re.sub(r'\s+', ' ', text)
    # Remove non-printable characters
    text = ''.join(c if c.isprintable() or c == '\n' else ' ' for c in text)
    return text


class OCRProcessingError(Exception):
    """Exception raised for errors in OCR processing"""
    pass
