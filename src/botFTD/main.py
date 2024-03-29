import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv , find_dotenv

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix = "?", 
    intents=intents
    )

async def load():
    dirname = os.path.dirname(__file__)
    filename = os.path.join(dirname, 'cogs')
    for file in os.listdir(filename):
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

load_dotenv(find_dotenv())

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('Token'))

asyncio.run(main())