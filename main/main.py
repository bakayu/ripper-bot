import discord
from discord.ext import commands
from utils.discord_helpers import fetch_message_images
from utils.ocr_processor import process_images_to_text
from utils.pdf_builder import create_pdf
import os

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)

@bot.command()
async def convert(ctx, message_id: int):
    """Convert message images to OCR PDF: !convert <message_id>"""
    try:
        # Fetch images from target message
        images = await fetch_message_images(ctx, message_id)
        
        if not images:
            await ctx.send("No valid images found in the specified message")
            return
            
        # Process images through OCR pipeline
        ocr_results = await process_images_to_text(images)
        
        # Create PDF with formatted text
        pdf_path = "output.pdf"
        create_pdf(ocr_results, pdf_path)
        
        # Send result
        await ctx.send(file=discord.File(pdf_path))
        os.remove(pdf_path)  # Cleanup
        
    except Exception as e:
        await ctx.send(f"Error: {str(e)}")

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
