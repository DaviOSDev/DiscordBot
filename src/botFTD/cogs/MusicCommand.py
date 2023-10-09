import yt_dlp
from discord.ext import commands
import discord

yt_dlp.utils.bug_reports_message = lambda: ''

ytdlFormmatOptions = {

    'format': 'bestaudio',
    'noplaylist': 'True',
    
}

ffmpegOptions = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}


ytdl = yt_dlp.YoutubeDL(ytdlFormmatOptions)

class MusicCommands(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.bot = bot
        self.queue = []
        self.isPlaying = False
        self.vc = None
        self.isPaused = False


    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands ready...")

    def searchyt(self, url):
        try:
            data = ytdl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
        except Exception:
            return False
        
        return {'source': data['url'], 'title': data['title']}

    def playnext(self):
        print(len(self.queue))
        if len(self.queue) > 0:
            self.isPlaying = True

            url = self.queue[0][0]['source']

            self.queue.pop(0)

            self.vc.play(source=discord.FFmpegPCMAudio(url, **ffmpegOptions,), after=lambda e:  self.playnext())
        else:
            self.isPlaying = False
        
    async def playMusic(self, ctx):
        if len(self.queue) > 0:
            self.isPlaying = True
            url = self.queue[0][0]['source']

            if self.vc == None or not self.vc.is_conected():
                self.vc = await self.queue[0][1].connect()

                if self.vc == None:
                    ctx.send("Could'nt connect to the channel")
                    return
            else:
                await self.vc.move_to(self.queue[0][1])
               

            self.queue.pop(0)
            self.vc.play(source=discord.FFmpegPCMAudio(url, **ffmpegOptions),  after= lambda e: self.playnext())
        else:
            self.isPlaying = False
            await self.leave(ctx=ctx)

    @commands.command(name="play", aliases= ["p"],  help="Plays from a youtube url")
    async def play(self, ctx, *args):
        
        url = args[0]
        voiceChannel = ctx.author.voice.channel
        if voiceChannel is None:
            await ctx.send("Connect to a voice channel first")
        
        elif self.isPaused:
            self.vc.resume()

        else: 
            song = self.searchyt(url)
        
        print(song) 

        if type(song) == type(True):
            await ctx.send("Could'nt download the song")
        else:
            await ctx.send(f"{song['title']} added to the queue")
            self.queue.append([song, voiceChannel])

            if self.isPlaying == False:
                await ctx.send(f"Now Playing: {self.queue[0][0]['title']}")
                await self.playMusic(ctx)

    @commands.command(name="pause", help="Pause the queue")
    async def Pause(self, ctx):
        if self.isPlaying:
            self.isPlaying = False
            self.isPaused = True
            self.vc.pause()

        elif self.isPaused:
            self.vc.resume()

    @commands.command(name="resume", help="resume the queue")
    async def resume(self, ctx):
        if self.isPaused:
            self.isPaused = False
            self.isPlaying = True
            self.vc.resume()

    async def leave(self, ctx):
        "disconnects the bot from voice"
        if self.vc.is_connected():
            print(f"leaving {self.vc}")
            await self.vc.disconnect()
            self.vc = None
        else:
            ctx.send("I'm not in a voice channel")

    @commands.command(name="clear-queue", aliases=['c', 'clearq'], help='Clears the queue')
    async def clear(self, ctx):
        print("Clearing queue...")
        self.queue = []
        await ctx.send("Music queue cleared")

    @commands.command(name="next", aliases=["skip"], help="skips the current music(if there's no other music it leaves the channel)")
    async def skip(self, ctx):
        if self.vc != None:
            await ctx.send("skiping music")
            self.vc.stop()
            await self.playMusic(ctx)

    @commands.command(name="show-queue", aliases = ["sq", "showq"], help="show the next 4 music in queue")
    async def showQueue(self, ctx):
        string = "```"
        if len(self.queue) == 0:
            await ctx.send("There's nothin in queue")
        
        elif len(self.queue) >= 4:
            for i in range(0,3):
                    string += f"{i+1} - " + self.queue[i][0]['title'] + "\n"
            
            string += "```"
            await ctx.send(string)
        
        else:
            for i in range(0, len(self.queue)):
                string += f"{i+1} - " + self.queue[i][0]['title'] + "\n"
            
            string += "```"
            await ctx.send(string)


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
