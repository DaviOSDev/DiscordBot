import random
from discord.ext import commands
import discord

class DiceCommands(commands.Cog):
    def __init__(self, bot):
        self.bot = bot

    @commands.Cog.listener()
    async def on_ready(self):
        print("Dice Commands ready...")

    @commands.command(name="Roll", aliases =["r"], help="Roll dices")
    async def roll(self, ctx, *arg):
        string = ""; total =  0
        try:
            for item in arg:
                
                item = self.prepareItem(item)
                
                if item[0] <= 0 or item[0] > 50:
                    raise Exception
                
                list = self.diceResult(item[0], item[1])
                string += f"d{item[1]} " + list[0]
                total += list[1]

            string += f"final Result ==> ({total})"
            await ctx.send(string) 
        except Exception as e:
            print(e)
            await ctx.send("Wrong template, try: ([ 0 < number <= 50 ]d[number > 0])...")

    @commands.command(name="rollshow", aliases=["rs", "r#", "roll#"], help="Roll dices and show the result of each one")
    async def rollshow(self, ctx, *arg):
        string = "";total = 0
        try:
            for item in arg:
                item = self.prepareItem(item)

                if item[0] <= 0 or item[0] > 50:
                    raise Exception

                list = self.showDiceResult(item[0], item[1])
                total += list[1]; string += list[0]
        
            string += f"total ==> ({total})"
            await ctx.send(string)
        except Exception as e:
            print(e)
            await ctx.send("Wrong template, try: ([ 0 < number <= 50 ]d[number > 0])...")

    def showDiceResult(self, numeroDeDados, dado):
        String = f'd{dado}:\n'; total = 0; count =1
        
        for _ in range(0, numeroDeDados):
            result = random.randint(1, dado)
            total += result
            String += f"    (dado {count}) -> {result}\n"
            count += 1
        String += f"    total (d{dado}) --> {total}\n"
        list = [String, total]
        return list

    def diceResult(self, numeroDeDados, dado):
        String = ''; count = 1; total = 0
        
        for _ in range(0, numeroDeDados):
            result = random.randint(1, dado)
            total += result
            count += 1
        String += f"total (d{dado}) -> {total}\n"
        list = [String, total]
        return list

    def prepareItem(self, item):
        item = item.split("d")
        
        if item[0] == '':
            item[0] = 1
        else:
            item[0] = int(item[0])
        item[1] = int(item[1])
        return item
    
async def setup(bot):
    await(bot.add_cog(DiceCommands(bot=bot)))