import os
import random
import aiohttp
import discord
from discord.ext import commands
from discord import app_commands

# === Discord Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True
bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# === Trigger Words and Emoji Mapping ===
TRIGGER_WORDS = {
    "goose", "bad", "kill", "run", "die", "honk", "hi", "sigma",
    "pickln", "potato", "cat", "gun", "shoot", "murder", "shoe",
    "nike", "smoke", "chill", "yap"
}

WORD_EMOJI_MAP = {
    "kill": "duck_killer",
    "bad": "goose_aggressive",
    "die": "duck_killer",
    "run": "duck_aggressive",
    "gun": "goosegun",
    "shoot": "goosegun",
    "murder": "goosegun",
    "shoe": "GooseSneaks",
    "nike": "GooseSneaks",
    "smoke": "goose_pipe",
    "chill": "goose_pipe",
    "honk": "honk4",
    "yap": "honk4",
    "pickln": "honk4"
}

DEFAULT_EMOJI_NAME = "goosealert"

EMOJI_IMAGES = {
    "goosealert": "https://cdn.discordapp.com/emojis/1337164459541790783.png",
    "duck_killer": "https://cdn.discordapp.com/emojis/1337164615443939430.png",
    "goose_aggressive": "https://cdn.discordapp.com/emojis/1337164458535157914.png",
    "GooseSneaks": "https://raw.githubusercontent.com/picklngoose/the-real-goosereactor/refs/heads/main/emojis/GooseSneaks.png",
    "goose_pipe": "https://raw.githubusercontent.com/picklngoose/the-real-goosereactor/refs/heads/main/emojis/goose_pipe.png",
    "goosegun": "https://raw.githubusercontent.com/picklngoose/the-real-goosereactor/refs/heads/main/emojis/goosegun.png",
    "honk4": "https://raw.githubusercontent.com/picklngoose/the-real-goosereactor/refs/heads/main/emojis/honk4.png"
}

# === Commands ===
@bot.command(name="help", help="Shows a list of trigger words and their effects.")
async def custom_help(ctx):
    embed = discord.Embed(
        title="🪶 Goose Bot Help",
        description="This bot reacts to certain words and phrases. Here's what it can do:",
        color=discord.Color.orange()
    )
    embed.add_field(
        name="🔁 Emoji Reactions",
        value=(
            "**goose** → :goosealert:\n"
            "**bad** → :goose_aggressive:\n"
            "**kill** → :duck_killer:\n"
            "**run** → :duck_aggressive:\n"
            "**die** → :duck_killer:\n"
            "**honk**, **hi**, **sigma**, **pickln**, **potato**, **cat** → :goosealert:"
        ),
        inline=False
    )
    embed.add_field(
        name="💬 Message Replies",
        value=(
            "**goose** → HONK\n"
            "**moose** → HISS\n"
            "**geese** → honk?\n"
            "**llama**, **turtle**, **dog** → ?\n"
            "**buke**, **cyber**, **sniper** → !\n"
            "**kill the goose** → [Goose Attack GIF](https://tenor.com/view/goose-attack-gif-26985079)\n"
            "**cat** + **goose** → [Goose vs Cat GIF](https://tenor.com/view/goose-gif-14930335269575530990)"
        ),
        inline=False
    )
    embed.add_field(
        name="❓ Yes/No Questions",
        value="Goose replies with an answer",
        inline=False
    )
    embed.set_footer(text="Trigger words are case-insensitive.")
    await ctx.send(embed=embed)

@bot.tree.command(name="goosefact", description="Learn a fun goose fact.")
async def goose_fact(interaction: discord.Interaction):
    facts = [
        "Geese fly in a V to conserve energy.",
        "Geese mate for life 💘.",
        "A group of geese on land is called a gaggle.",
        "Geese are very protective parents.",
        "Geese have excellent eyesight!",
        "Geese can remember people — friend or foe!",
        "Some geese can fly over 5,000 miles during migration!",
        "The Canada goose is one of the most widespread species in North America.",
        "Baby geese are called goslings 🐣.",
        "Geese can live 10–25 years in the wild.",
        "Geese honk to communicate while flying to keep the group together.",
        "Geese can be trained — they’re very smart animals!",
        "In Ancient Egypt, geese were considered sacred animals.",
        "Some geese have been known to guard homes like dogs 🏠.",
        "Geese form strong social bonds and mourn when one dies."
    ]
    await interaction.response.send_message("🪶 " + random.choice(facts))

# === Events ===
@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")
    print(f"🔗 Connected to {len(bot.guilds)} server(s):")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id})")

    try:
        # Remove old slash command "goose" if it exists
        commands = await bot.tree.fetch_commands()
        for cmd in commands:
            if cmd.name == "goose":
                await bot.tree.remove_command(cmd.name, type=discord.AppCommandType.chat_input)
                print(f"❌ Removed slash command: /{cmd.name}")

        # Sync new slash commands
        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")

@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # Detect and respond to yes/no questions
    yes_no_starters = (
        "is", "are", "do", "does", "did", "will", "would", "can", "could",
        "should", "shall", "am", "was", "were", "have", "has", "had"
    )
    if content.startswith(yes_no_starters) and content.endswith("?"):
        await message.channel.send("https://tenor.com/view/no-nope-denied-goose-gif-25891503")
        return

    # React to trigger words with emojis
    for word in TRIGGER_WORDS:
        if word in content:
            emoji_name = WORD_EMOJI_MAP.get(word, DEFAULT_EMOJI_NAME)
            emoji = await get_or_create_emoji(message.guild, emoji_name)
            if emoji:
                await message.add_reaction(emoji)

    # Text responses
    if "goose" in content:
        await message.channel.send("HONK")
    if "moose" in content:
        await message.channel.send("HISS")
    if "geese" in content:
        await message.channel.send("honk?")
    if any(x in content for x in ["llama", "turtle", "dog"]):
        await message.channel.send("?")
    if any(x in content for x in ["buke", "cyber", "sniper"]):
        await message.channel.send("!")
    if "kill the goose" in content:
        await message.channel.send("https://tenor.com/view/goose-attack-gif-26985079")
    if "cat" in content and "goose" in content:
        await message.channel.send("https://tenor.com/view/goose-gif-14930335269575530990")

    await bot.process_commands(message)

# === Emoji Creation Helper ===
async def get_or_create_emoji(guild: discord.Guild, emoji_name: str) -> discord.Emoji | None:
    for emoji in guild.emojis:
        if emoji.name == emoji_name:
            return emoji

    url = EMOJI_IMAGES.get(emoji_name)
    if not url:
        return None

    try:
        async with aiohttp.ClientSession() as session:
            async with session.get(url) as resp:
                if resp.status == 200:
                    image_data = await resp.read()
                    return await guild.create_custom_emoji(name=emoji_name, image=image_data)
    except Exception as e:
        print(f"❌ Failed to create emoji '{emoji_name}': {e}")

    return None

# === Start Bot ===
bot.run(os.environ["DISCORD_BOT_TOKEN"])
