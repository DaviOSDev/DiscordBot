import discord
from discord.ext import commands
import random
import os
from dotenv import load_dotenv , find_dotenv
from PIL import Image, ImageDraw, ImageFont, ImageOps
from io import BytesIO

bot = commands.Bot('?')

load_dotenv(find_dotenv())
    
fonte = ImageFont.truetype('Shiver Me Timbers NF.ttf', 35)
fonte_numeros = ImageFont.truetype('Awaken.otf',23)

@bot.event
async def on_ready():
    print(f"Logged as {bot.user}!")

@bot.command()
async def roll(ctx, arg):
    try:
        arg = int(arg)
        n = random.randint(1, arg)
        dado_image = Image.open("Dado.png")
        dado_draw = ImageDraw.Draw(dado_image)
        dado_draw.line(((18), (182))) #x
        dado_draw.line(((9), (191))) #y
        fonte_numeros = ImageFont.truetype('Awaken.otf',50)
        dado_draw.text(xy=(100, 110), text=f"{n}", fill=(255, 255, 255), anchor= "mm", font=fonte_numeros)
        bytes_dado = BytesIO()
        dado_image.save(bytes_dado, format="PNG")
        bytes_dado.seek(0)
        dado_file = discord.File(bytes_dado, filename="dado_imageMOD.png")
        await ctx.send(file= dado_file)
    except:
        await ctx.send("PARA DE MANDAR LETRA FDP")

@bot.command()
async def char(ctx, arg):
    
    image = Image.open('Ficha.png')
    first_name = ['Lakye', 'Debora' ,'Yasmin', 'Rogerio', 'Will', 'Abigail', 'Zeke', 'Daenerys', 'Jason', 'Albert', 'Jack', 'Marie', 'Nickola']
    last_name = ['Tesla', 'Curie', 'Mesquita', 'Costa', 'Bourbon', 'Uchoas', 'Lopes', 'Firmino', 'Olivier']

    strengh = random.randint(1, 20)
    intelligence = random.randint(1, 20)
    wisdom = random.randint(1, 20)
    dexterity = random.randint(1, 20)
    constitution = random.randint(1, 20)
    charm = random.randint(1, 20)
    name = ImageDraw.Draw(image)

    strengh_draw = ImageDraw.Draw(image)
    intelligence_draw = ImageDraw.Draw(image)
    wisdom_draw = ImageDraw.Draw(image)
    dexterity_draw = ImageDraw.Draw(image)
    constitution_draw = ImageDraw.Draw(image)
    charm_draw = ImageDraw.Draw(image)

    strengh_draw.line(((285), (317))) #x
    strengh_draw.line(((77), (112))) #y
    intelligence_draw.line = strengh_draw.line #x
    intelligence_draw.line(((139), (174))) #y
    wisdom_draw.line = strengh_draw.line #x
    wisdom_draw.line(((203), (236))) #y
    dexterity_draw.line = strengh_draw.line #x
    dexterity_draw.line(((270), (303))) #y
    constitution_draw.line = strengh_draw.line #x
    constitution_draw.line(((333), (365))) #y
    charm_draw.line = strengh_draw.line #x
    charm_draw.line(((393), (426))) #y

    if arg == 'aleatorio':
        name.text(xy=(100, 20), text =f"{random.choice(first_name)} {random.choice(last_name)}", fill=(0, 0, 120), font= fonte)
    else:
        nome = arg.split('_')
        nome_junto = ' '.join(nome)
        name.text(xy=(100, 20), text = arg, fill=(0, 0, 120), font= fonte)
    strengh_draw.text(xy=(301, 94.5), text =f"{strengh}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    intelligence_draw.text(xy=(301, 160), text =f"{intelligence}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    wisdom_draw.text(xy=(301, 222), text =f"{wisdom}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    dexterity_draw.text(xy=(301, 288), text =f"{dexterity}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    constitution_draw.text(xy=(301, 352), text =f"{constitution}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    charm_draw.text(xy=(301, 410), text =f"{charm}", fill=(0, 0, 120), anchor = 'mm' ,font= fonte_numeros)
    
    bytes = BytesIO()
    image.save(bytes, format="PNG")
    bytes.seek(0)
    dfile = discord.File(bytes, filename="ImageMOD.png")
    
    await ctx.send("Character made =", file= dfile)

@bot.command()
async def Luciana(ctx):
    await ctx.send('CALVISSIMA')

@bot.command()
async def Joao(ctx):
    await ctx.send("O JAO E FODA")

@bot.command()
async def Tobi(ctx):
    await ctx.send('ANAOZINHO')

@bot.command()
async def Guilherme(ctx):
    Gui = "Guilherme.jpeg"
    guifile = discord.File(Gui, filename="Guilhermer.jpeg")
    await ctx.send(file= guifile)

@bot.command()
async def Ze(ctx):
    Zefile = discord.File("Ze.jpeg", filename="Zezinho.jpeg")
    await ctx.send(file= Zefile)


bot.run(os.getenv('Token'))