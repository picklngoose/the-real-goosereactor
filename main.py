import os
import discord
from discord.ext import commands
from flask import Flask
from threading import Thread
import aiohttp

# === Web Server Setup ===
app = Flask('')

@app.route('/')
def home():
    return "Goose reactor is alive!"

def run_web_server():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run_web_server)
    t.start()

# === Discord Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents)

TRIGGER_WORDS = {"goose", "bad", "kill", "run", "die", "honk", "hi", "sigma", "pickln", "potato", "cat"}

# Map specific trigger words to emoji names
WORD_EMOJI_MAP = {
    "kill": "duck_killer",
    "bad": "goose_aggressive",
    "die": "duck_killer",
    "run": "duck_aggressive"
}
DEFAULT_EMOJI_NAME = "goosealert"

# Emoji image URLs (replace with your own if needed)
EMOJI_IMAGES = {
    "goosealert": "https://cdn.discordapp.com/emojis/1337164459541790783.png",
    "duck_killer": "https://cdn.discordapp.com/emojis/1337164615443939430.png",
    "goose_aggressive": "https://cdn.discordapp.com/emojis/1337164458535157914.png"
}

async def get_or_create_emoji(guild: discord.Guild, emoji_name: str) -> discord.Emoji | None:
    # Check if emoji already exists
    for emoji in guild.emojis:
        if emoji.name == emoji_name:
            return emoji

    # Get emoji image URL
    url = EMOJI_IMAGES.get(emoji_name)
    if not url:
        return None

    # Try downloading the image and creating the emoji
    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    return await guild.create_custom_emoji(name=emoji_name, image=image_data)
    except Exception as e:
        print(f"❌ Failed to create emoji '{emoji_name}': {e}")
    return None

@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    for word in TRIGGER_WORDS:
        if word in content:
            emoji_name = WORD_EMOJI_MAP.get(word, DEFAULT_EMOJI_NAME)
            emoji = await get_or_create_emoji(message.guild, emoji_name)
            if emoji:
                await message.add_reaction(emoji)

    if "goose" in content:
        await message.channel.send("HONK")

    if "moose" in content:
        await message.channel.send("HISS")

    if "geese" in content:
        await message.channel.send("honk?")

    if "llama" in content:
        await message.channel.send("?")

    await bot.process_commands(message)

# === Run Server and Bot ===
keep_alive()
bot.run(os.environ["DISCORD_BOT_TOKEN"])
