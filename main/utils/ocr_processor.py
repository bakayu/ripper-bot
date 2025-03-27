import pytesseract
from PIL import Image, ImageOps
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

        # Check image width and downscale if too wide
        max_width = 1800  # Maximum width in pixels
        if image.width > max_width:
            # Calculate new size while maintaining aspect ratio
            new_width = max_width
            new_height = int(image.height * (max_width / image.width))
            image = image.resize((new_width, new_height), Image.LANCZOS)

        # Preprocess image
        image = image.convert('L')  # Convert to grayscale
        image = ImageOps.autocontrast(image)  # Improve contrast

        # Simplified config with special character support
        custom_config = '--oem 3 --psm 6 -c tessedit_char_whitelist="ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz0123456789.,!?()@:;\'\"\\-—_*$#%&+=/<> "'

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
    """Clean and correct OCR output"""
    import re

    # Fix common asterisk misreadings
    text = re.sub(r'\bseek\b', '***', text)
    text = re.sub(r'\beek\b', '***', text)
    text = re.sub(r'\bkkk\b', '***', text)

    # Fix spaces around asterisks
    text = re.sub(r'\s*\*\s*\*\s*\*\s*', ' *** ', text)

    # Fix consecutive asterisks
    text = re.sub(r'\*(\s*\*)+', '***', text)

    return text.strip()


class OCRProcessingError(Exception):
    pass
