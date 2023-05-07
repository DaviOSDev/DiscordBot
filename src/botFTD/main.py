import os
from discord.ext import commands
from dotenv import load_dotenv , find_dotenv
from Commands import commandFunctions, IACommands
from CodeTools import functions

bot = commands.Bot('?')

load_dotenv(find_dotenv())

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}!")

@bot.command()
async def char(ctx, *arg):
    arg = functions.transformTupleToString(arg)
    await commandFunctions.char(ctx, arg)

@bot.command()
async def roll(ctx, arg):
    await commandFunctions.roll(ctx, arg)

@bot.command()
async def ask(ctx, *arg):
    arg = functions.transformTupleToString(arg)
    await IACommands.askCommand(ctx, arg)

bot.run(os.getenv('Token'))