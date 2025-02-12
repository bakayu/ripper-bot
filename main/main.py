import discord
from discord.ext import commands, app_commands
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
# Requires mod permissions
@app_commands.checks.has_permissions(manage_messages=True)
async def convert(
    interaction: discord.Interaction,
    message_id: str,
    filename: str = "output"
):
    try:
        await interaction.response.defer()

        msg_id = int(message_id)
        images = await fetch_message_images(interaction, msg_id)

        if not images:
            await interaction.followup.send("No valid images found in the specified message")
            return

        ocr_results = await process_images_to_text(images)
        pdf_path = f"{filename}.pdf"
        txt_path = f"{filename}.txt"

        formatted_text = create_pdf(ocr_results, pdf_path)

        # Save formatted text to .txt file
        with open(txt_path, 'w', encoding='utf-8') as f:
            f.write(formatted_text)

        # Send both files
        await interaction.followup.send(
            files=[
                discord.File(pdf_path),
                discord.File(txt_path)
            ]
        )

        # Cleanup
        os.remove(pdf_path)
        os.remove(txt_path)

    except app_commands.errors.MissingPermissions:
        await interaction.response.send_message("You need moderator permissions to use this command.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")


@bot.event
async def setup_hook():
    await bot.tree.sync()

if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
