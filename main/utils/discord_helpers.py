import httpx
import discord
import asyncio


async def fetch_message_images(interaction, message_id):
    """Fetch and validate images from Discord message"""
    try:
        message = await interaction.channel.fetch_message(message_id)
        return await download_images(message.attachments)
    except discord.NotFound:
        raise ValueError("Message not found")


async def download_images(attachments):
    """Download image attachments concurrently"""
    async with httpx.AsyncClient() as client:
        tasks = []
        for att in attachments:
            if any(att.filename.lower().endswith(ext) for ext in ['.png', '.jpg', '.jpeg']):
                tasks.append(client.get(att.url))

        responses = await asyncio.gather(*tasks)
        return [r.content for r in responses if r.status_code == 200]
