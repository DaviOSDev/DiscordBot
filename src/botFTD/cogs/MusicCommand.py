import yt_dlp
from discord.ext import commands
import discord
import asyncio

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
            print(self.queue[0])

            url = self.queue[0][0]['source']
            
            self.queue.pop(0)

            self.vc.play(source=discord.FFmpegPCMAudio(url, **ffmpegOptions,), after=lambda e: self.playnext())
        else:
            self.isPlaying = False
        
    async def playMusic(self, ctx):
        if len(self.queue) > 0:
            self.isPlaying = True
            url = self.queue[0][0]['source']

            print(url)
            print(len(self.queue))

            if self.vc == None or not self.vc.is_conected():
                self.vc = await self.queue[0][1].connect()

                if self.vc == None:
                    ctx.send("Could'nt connect to the channel")
                    return
            else:
                await self.vc.move_to(self.queue[0][1])

            self.queue.pop(0)

            self.vc.play(source=discord.FFmpegPCMAudio(url, **ffmpegOptions),  after= lambda e:  self.playnext())
        else:
            self.isPlaying = False


    @commands.command(name="play", aliases= ["p"],  help="Plays from a youtube url")
    async def play(self, ctx, *args):
        
        url = args[0]
        print(url)
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
                await self.playMusic(ctx)
                print(self.vc)


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

    @commands.command(pass_context=True)
    async def leave(self, ctx):
        "disconnects the bot from voice"

        if ctx.voice_client:
            print(f"leaving {ctx.guild.voice_client.channel}")
            await ctx.guild.voice_client.disconnect()
        else:
            ctx.send("I'm not in a voice channel")

    @commands.command(name="clear_queue", aliases=['c', 'clearq'], help='Clears the queue')
    async def clear(self, ctx):
        if self.vc != None and self.is_playing:
            self.vc.stop()
        self.music_queue = []
        await ctx.send("Music queue cleared")


async def setup(bot):
    await bot.add_cog(MusicCommands(bot))
