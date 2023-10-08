import os
from discord.ext import commands
from dotenv import load_dotenv , find_dotenv
from Commands import DiceCommand

bot = commands.Bot('?')

load_dotenv(find_dotenv())

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}!")

@bot.command(description= "Roll dices and shows the result")
async def roll(ctx, *arg,):
    await DiceCommand.roll(ctx, arg)

@bot.command(description="Roll dices and show the result of each dice")
async def rollshow(ctx, *arg,):
    await DiceCommand.rollshow(ctx, arg)

bot.run(os.getenv('Token'))