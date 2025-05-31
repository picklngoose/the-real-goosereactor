import os
import discord
from discord.ext import commands, tasks
from discord import app_commands
import aiohttp
import random
import asyncio

# === Discord Bot Setup ===
intents = discord.Intents.default()
intents.message_content = True

bot = commands.Bot(command_prefix="!", intents=intents, help_command=None)

# === Activity Status Rotation ===
activity_messages = [
    "Hunting for bread 🍞",
    "Hissing at cats 🐱",
    "Honking loudly 🎺",
    "Guarding the pond 🩺",
    "Flying around ✈️",
    "Looking for trouble 🙀",
    "Murdering moose 🫎",
    "Plotting world domination 🌍",
    "Inspecting shoes 👟",
    "if you have me in your server, you are lucky! only 100 servers max have me!!"🪿,
    "Use !help for some help 🪿",
    "Official server: https://discord.gg/8scYzHH9PN🪿"
]

@tasks.loop(hours=1)
async def update_status():
    new_status = random.choice(activity_messages)
    await bot.change_presence(activity=discord.CustomActivity(name=new_status))

# === Help Command ===
@bot.command(name="help", help="Shows a list of trigger words and their effects.")
async def custom_help(ctx):
    embed = discord.Embed(
        title="🩶 Goose Bot Help",
        description="This bot reacts to certain words and phrases. Here's what it can do:",
        color=discord.Color.green()
    )

    # Emoji Reactions
    emoji_reactions = {
        "goose": "goosealert",
        "bad": "goose_aggressive",
        "kill": "duck_killer",
        "run": "duck_aggressive",
        "die": "duck_killer",
        "gun / shoot / murder": "goosegun",
        "shoe / nike": "GooseSneaks",
        "smoke / chill": "goose_pipe",
        "honk / pickln / yap": "honk4",
        "hi / sigma / potato / cat": "goosealert"
    }

    emoji_desc = "\n".join(f"**{words}** → :{emoji}:" for words, emoji in emoji_reactions.items())
    embed.add_field(name="🔁 Emoji Reactions", value=emoji_desc, inline=False)

    # Message Replies
    message_replies = {
        "**goose**": "HONK",
        "**moose**": "HISS",
        "**geese**": "honk?",
        "**llama**, **turtle**, **dog**": "?",
        "**buke**, **cyber**, **sniper**": "!",
        "**kill the goose**": "[Goose Attack GIF](https://tenor.com/view/goose-attack-gif-26985079)",
        "**cat** + **goose**": "[Goose vs Cat GIF](https://tenor.com/view/goose-gif-14930335269575530990)"
    }

    reply_desc = "\n".join(f"{k} → {v}" for k, v in message_replies.items())
    embed.add_field(name="💬 Message Replies", value=reply_desc, inline=False)

    embed.add_field(
        name="❓ Yes/No Questions",
        value="Goose replies with a GIF answer if your message starts like a question and ends with a `?`.",
        inline=False
    )

    embed.set_footer(text="If you have me in your server, you are lucky! Only 100 servers max can have a goose like me! Official server: https://discord.gg/8scYzHH9PN")
    await ctx.send(embed=embed)

# === Triggers and Emoji Mapping ===
TRIGGER_WORDS = {
    "goose", "bad", "kill", "run", "die", "honk", "hi", "sigma", "pickln",
    "potato", "cat", "gun", "shoot", "murder", "shoe", "nike", "smoke", "chill",
    "yap"
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

async def get_or_create_emoji(guild: discord.Guild, emoji_name: str) -> discord.Emoji | str | None:
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
    except discord.Forbidden:
        print(f"⚠️ Forbidden: Cannot create emoji '{emoji_name}' — using fallback.")
        return "🪿"
    except Exception as e:
        print(f"❌ Failed to create emoji '{emoji_name}': {e}")

    return None

# === /goosefact Slash Command ===
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
        "Baby geese are called goslings 👧.",
        "Geese can live 10–25 years in the wild.",
        "Geese honk to communicate while flying to keep the group together.",
        "Geese can be trained — they’re very smart animals!",
        "In Ancient Egypt, geese were considered sacred animals.",
        "Some geese have been known to guard homes like dogs 🏠.",
        "Geese form strong social bonds and mourn when one dies."
    ]
    await interaction.response.send_message("🪶 " + random.choice(facts))

# === Bot Ready Event ===
@bot.event
async def on_ready():
    print(f"✅ Bot is ready. Logged in as {bot.user}")
    print(f"🔗 Connected to {len(bot.guilds)} server(s):")
    for guild in bot.guilds:
        print(f" - {guild.name} (ID: {guild.id})")

    try:
        commands = await bot.tree.fetch_commands()
        for cmd in commands:
            if cmd.name == "goose":
                await bot.tree.remove_command(cmd.name, type=discord.AppCommandType.chat_input)
                print(f"❌ Removed slash command: /{cmd.name}")

        synced = await bot.tree.sync()
        print(f"🔄 Synced {len(synced)} slash commands.")
    except Exception as e:
        print(f"❌ Error syncing slash commands: {e}")

    update_status.start()

# === Message Listener ===
@bot.event
async def on_message(message):
    if message.author.bot:
        return

    content = message.content.lower()

    # Yes/No Question Detection
    yes_no_starters = (
        "is", "are", "do", "does", "did", "will", "would", "can", "could",
        "should", "shall", "am", "was", "were", "have", "has", "had"
    )
    if content.startswith(yes_no_starters) and content.endswith("?"):
        await message.channel.send("https://tenor.com/view/no-nope-denied-goose-gif-25891503")
        return

    # Trigger Word Emoji Reactions
    for word in TRIGGER_WORDS:
        if word in content:
            emoji_name = WORD_EMOJI_MAP.get(word, DEFAULT_EMOJI_NAME)
            emoji = await get_or_create_emoji(message.guild, emoji_name)

            try:
                if isinstance(emoji, discord.Emoji):
                    await message.add_reaction(emoji)
                elif isinstance(emoji, str):
                    await message.add_reaction(emoji)
            except discord.HTTPException as e:
                print(f"❌ Could not add reaction: {e}")

    # Text Replies
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

# === Run Bot ===
bot.run(os.environ["DISCORD_BOT_TOKEN"])
