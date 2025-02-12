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

        custom_config = r'''
            --oem 3 --psm 11
            -c preserve_interword_spaces=1 
            textord_space_size_is_variable=1 
            textord_min_space_size=20  # Minimum pixel gap between words
            textord_heavy_nr=1  # Aggressive noise removal
            thresholding_method=2  # Automatic adaptive threshold
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
    """ripped by jack"""
    return text.strip()


class OCRProcessingError(Exception):
    pass
