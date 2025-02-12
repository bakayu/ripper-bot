from fpdf import FPDF
import pyphen
import google.generativeai as genai
import os
from dotenv import load_dotenv
from datetime import datetime

load_dotenv()
genai.configure(api_key=os.getenv("GEMINI_API_KEY"))
model = genai.GenerativeModel('gemini-2.0-flash')


class GeminiFormatter:
    def format_text(self, text: str) -> str:
        """Use Gemini for text formatting and refinement"""
        response = model.generate_content(f"""
        Format this text into clean paragraphs with proper line breaks and punctuation.
        Preserve all original content (output should not be in italics):
        
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
    print(text_contents)
    formatted_text = formatter.format_text("\n".join(text_contents))

    pdf = NoMetaPDF()
    pdf.add_page()

    # Increase page width margins
    pdf.set_margins(20, 15, 20)
    pdf.set_auto_page_break(True, margin=15)

    for paragraph in formatted_text.split('\n\n'):
        if paragraph.strip():
            print(paragraph, '\n')
            # Set alignment based on content length
            pdf.set_font('NotoSans', size=11)  # Slightly reduce font size

            # Handle long words by using justified alignment
            pdf.set_font_size(11)
            pdf.set_x(20)  # Reset x position
            pdf.multi_cell(0, 6, paragraph.strip(), align='J',
                           border=0, markdown=False)
            pdf.ln(4)

    pdf.output(output_path)
