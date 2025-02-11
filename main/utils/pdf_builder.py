import pytesseract
from PIL import Image
import io
import asyncio

async def process_images_to_text(images):
    """Process images through AI-powered OCR pipeline"""
    tasks = [process_single_image(img) for img in images]
    return await asyncio.gather(*tasks)

async def process_single_image(image_data):
    """Enhanced OCR processing with AI components"""
    try:
        image = Image.open(io.BytesIO(image_data))
        
        # AI-enhanced OCR configuration
        custom_config = r'''
            --oem 3 --psm 6
            -c tessedit_char_whitelist=ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789-.,!?()@:;'"/\\%$
            preserve_interword_spaces=1
        '''
        
        text = pytesseract.image_to_string(
            image,
            lang='eng',
            config=custom_config
        )
        
        return post_process_text(text)
        
    except Exception as e:
        raise OCRProcessingError(f"OCR failed: {str(e)}")

def post_process_text(text):
    """AI-powered text cleaning and formatting"""
    # Add your custom NLP processing here
    return text.strip()

class OCRProcessingError(Exception):
    pass
