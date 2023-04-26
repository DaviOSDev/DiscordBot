import random
import os
import discord
from discord.ext import commands
from dotenv import load_dotenv , find_dotenv
from PIL import Image, ImageDraw, ImageFont
from io import BytesIO
import commandFunctions as CF

bot = commands.Bot('?')

load_dotenv(find_dotenv())

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}!")

@bot.command()
async def char(ctx, arg='aleatorio'):
    await CF.char(ctx, arg)

@bot.command()
async def roll(ctx, arg):
    await CF.roll(ctx, arg)

bot.run(os.getenv('Token'))