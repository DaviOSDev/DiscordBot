import os
import asyncio
import discord
from discord.ext import commands
from dotenv import load_dotenv , find_dotenv
from Commands import DiceCommand
import time

intents = discord.Intents.default()
intents.message_content = True
intents.voice_states = True

bot = commands.Bot(
    command_prefix = "?", 
    intents=intents
    )

async def load():
    for file in os.listdir("C:/Users/davik/OneDrive/Desktop/Projetos/DiscordBot/src/botFTD/cogs"):
        print(file)
        if file.endswith(".py"):
            await bot.load_extension(f"cogs.{file[:-3]}")

load_dotenv(find_dotenv())

@bot.command(description= "Roll dices and shows the result")
async def roll(ctx, *arg,):
    await DiceCommand.roll(ctx, arg)

@bot.command(description="Roll dices and show the result of each dice")
async def rollshow(ctx, *arg,):
    await DiceCommand.rollshow(ctx, arg)

@bot.event
async def on_ready():
    print(f'Logged in as {bot.user} (ID: {bot.user.id})')
    print('------')

async def main():
    async with bot:
        await load()
        await bot.start(os.getenv('Token'))

asyncio.run(main())