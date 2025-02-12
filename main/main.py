import discord
from discord.ext import commands
from utils.discord_helpers import fetch_message_images
from utils.ocr_processor import process_images_to_text
from utils.pdf_builder import create_pdf
import os
from dotenv import load_dotenv

load_dotenv()

intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix='!', intents=intents)


@bot.tree.command(name="rip", description="images to PDF")
async def convert(
    interaction: discord.Interaction,
    message_id: str,
    filename: str = "output"
):
    """Convert message images to OCR using message ID"""
    try:
        await interaction.response.defer()

        msg_id = int(message_id)
        images = await fetch_message_images(interaction, msg_id)

        if not images:
            await interaction.followup.send("No valid images found in the specified message")
            return

        ocr_results = await process_images_to_text(images)
        pdf_path = f"{filename}.pdf"
        create_pdf(ocr_results, pdf_path)

        await interaction.followup.send(file=discord.File(pdf_path))
        os.remove(pdf_path)
        print(f"{filename}.pdf created and uploaded successfully")

    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")


@bot.event
async def setup_hook():
    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
