import aspose.words as aw
from dotenv import load_dotenv
import os
from utils.pdf_builder import create_pdf
from utils.ocr_processor import process_images_to_text
from utils.discord_helpers import fetch_message_images
from discord import app_commands
from discord.ext import commands
import discord


load_dotenv()
os.environ["DOTNET_SYSTEM_GLOBALIZATION_INVARIANT"] = "1"


doc = aw.Document()
builder = aw.DocumentBuilder(doc)

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
                # discord.File(pdf_path),
                discord.File(txt_path)
            ]
        )

        # Cleanup
        os.remove(pdf_path)
        os.remove(txt_path)

    except discord.app_commands.errors.MissingPermissions:
        await interaction.response.send_message("You need moderator permissions to use this command.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")


@bot.tree.command(name="jack", description="Convert txt file to epub")
@app_commands.checks.has_permissions(manage_messages=True)
async def jack_convert(
    interaction: discord.Interaction,
    message_id: str
):
    try:
        await interaction.response.defer()

        msg_id = int(message_id)
        message = await interaction.channel.fetch_message(msg_id)

        if not message.attachments:
            await interaction.followup.send("No attachments found in the specified message")
            return

        txt_file = None
        for attachment in message.attachments:
            if attachment.filename.lower().endswith('.txt'):
                txt_file = attachment
                break

        if not txt_file:
            await interaction.followup.send("No .txt file found in the specified message")
            return

        content = await txt_file.read()
        txt_content = content.decode('utf-8')

        base_filename = os.path.splitext(txt_file.filename)[0]

        temp_txt_path = f"{base_filename}.txt"
        with open(temp_txt_path, 'w', encoding='utf-8') as f:
            f.write(txt_content)

        doc = aw.Document(temp_txt_path)
        epub_path = f"{base_filename}.epub"
        doc.save(epub_path, aw.SaveFormat.EPUB)

        await interaction.followup.send(file=discord.File(epub_path))

        os.remove(temp_txt_path)
        os.remove(epub_path)

    except discord.app_commands.errors.MissingPermissions:
        await interaction.response.send_message("You need moderator permissions to use this command.", ephemeral=True)
    except Exception as e:
        await interaction.followup.send(f"Error: {str(e)}")


@bot.event
async def setup_hook():
    await bot.tree.sync()


if __name__ == "__main__":
    bot.run(os.getenv("DISCORD_TOKEN"))
