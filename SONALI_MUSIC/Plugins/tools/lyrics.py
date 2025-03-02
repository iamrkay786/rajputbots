from pyrogram import Client, filters
from pyrogram.enums import ParseMode
from pyrogram.types import Message
import requests
from SONALI_MUSIC import app

# API base URL
API_BASE_URL = "https://song.codesearch.workers.dev/?name="

@app.on_message(filters.command("lyrics"))
async def fetch_song(client, message: Message):
    # Extract the song name from the command
    if len(message.command) < 2:
        await message.reply_text("Please provide a song name. Example: /lyrics Yad")
        return

    song_name = " ".join(message.command[1:])
    response = requests.get(API_BASE_URL + song_name)

    if response.status_code == 200:
        data = response.json()
        # Check if the API response is successful and contains results
        if data.get("success") and data["data"]["data"]["results"]:
            # Get the first song from the results
            song = data["data"]["data"]["results"][0]
            song_name = song["name"]
            song_url = song["url"]
            download_links = song.get("downloadUrl", [])  # Get the download links (list of dictionaries)
            artist = song["artists"]["primary"][0]["name"]

            # Prepare the reply message
            reply = (
                f"🎶 {song_name}\n"
                f"👤 Artist: {artist}\n"
                f"🔗 [Listen here]({song_url})\n"
            )

            # Add download links if available
            if download_links:
                reply += "⬇️ Download here:\n"
                for link in download_links:
                    quality = link.get("quality", "Unknown Quality")
                    url = link.get("url", "#")
                    reply += f"   - [{quality}]({url})\n"
            else:
                reply += "⬇️ Download link not available."

            # Send the reply with Markdown formatting
            await message.reply_text(reply, parse_mode=ParseMode.MARKDOWN)
        else:
            await message.reply_text("Sorry, I couldn't find any results for that song.")
    else:
        await message.reply_text("An error occurred while fetching the song. Please try again later.")
