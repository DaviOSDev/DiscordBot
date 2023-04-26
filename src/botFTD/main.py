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

bot.run('MTAwODIyNTE4Mjg0ODEyNzAxNg.Gp7GRS.nUYsl1n0w4UuB35iJCaZp30Q7U1rGOTOz7hw5w')