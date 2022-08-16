import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv , find_dotenv

bot = commands.Bot('?')

load_dotenv(find_dotenv())

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}!")

@bot.command()
async def roll(ctx, arg):
    try:
        arg = int(arg)
        n = random.randint(1, arg)
        await ctx.send(f'O valor do d{arg} foi: {n}!')
    except:
        await ctx.send('MANDA LETRA N ARROMBADO')

@bot.command()
async def char(ctx):
    first_name = ['Lakye', 'Debora' ,'Yasmin', 'Rogerio', 'Will', 'Abigail', 'Zeke', 'Daenerys', 'Jason', 'Albert', 'Jack', 'Marie', 'Nickola']
    last_name = ['Tesla', 'Curie', 'Mesquita', 'Costa', 'Bourbon', 'Uchoas', 'Lopes', 'Firmino', 'Olivier']
    strengh = random.randint(1, 20)
    wisdom = random.randint(1, 20)
    intelligence = random.randint(1, 20)
    charisma = random.randint(1, 20)
    dexterity = random.randint(1, 20)
    await ctx.send(f'O personagem :{random.choice(first_name)} {random.choice(last_name)} tem...\n strengh = {strengh}')

@bot.command()
async def Luciana(ctx):
    await ctx.send('CALVISSIMA')

@bot.command()
async def Joao(ctx):
    await ctx.send('O jao eh delicioso')

@bot.command()
async def Tobi(ctx):
    await ctx.send('ANAOZINHO')





bot.run(os.getenv('Token'))