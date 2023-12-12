import yt_dlp
from discord.ext import commands, tasks
import discord
import threading
import asyncio

yt_dlp.utils.bug_reports_message = lambda: ''


ytdlFormmatOptions = {

    'format': 'bestaudio',
    'noplaylist': True,
    "ignoreerrors": True,
    "quiet": True,
    "skip_download": True,
    "no_warnings": True,
    "playlist_items": "1",
}




ffmpegOptions = {'before_options': '-reconnect 1 -reconnect_streamed 1 -reconnect_delay_max 5', 'options': '-vn'}

class MusicCommands(commands.Cog):

    def __init__(self, bot: commands.Bot):
        self.ytdl = yt_dlp.YoutubeDL(ytdlFormmatOptions)
        self.bot = bot
        self.queue = []
        self.isPlaying : bool = False
        self.vc = None
        self.isPaused : bool= False
        self.volume : float = 0.7
        self.musicTime : int = 0
        self.changeLoopTime : bool = False
        self.ctx = None
        self.currentSong : str = ""

    @tasks.loop()
    async def checkIsPlaying(self):
        print("checkIsPlaying loop started")
        if self.changeLoopTime:
            await self.ctx.send(f":microphone:  Now playing: {self.currentSong}")
            print(f"changing loop time to : {self.musicTime - 1}")
            self.checkIsPlaying.change_interval(seconds=self.musicTime - 1)
            print("loop time changed")
            self.changeLoopTime = False
            print(self.changeLoopTime)
        else:
            print("checking if is playing...")
            if self.isPlaying:
                print("is playing")
                self.checkIsPlaying.change_interval(seconds=0.5)
                pass
            else:
                print("is not playing, leaving channel...")
                await self.leave()
            
    @commands.Cog.listener()
    async def on_ready(self):
        print("Music commands ready...")

    async def checkVoiceChannel(self, ctx):
        if self.vc == None or not self.vc.is_conected():
                self.vc = await self.queue[0][1].connect()

                if self.vc == None:
                    ctx.send("Could'nt connect to the channel")
                    return
        elif self.vc != ctx.author.voice.channel:
            await self.vc.move_to(self.queue[0][1])
            return ctx.author.voice.channel

        else:
            return self.vc
                
    def searchyt(self, url):
        try:
            data = self.ytdl.extract_info(f"ytsearch:{url}", download=False)['entries'][0]
        except Exception:
            return False
        return {'source': data['url'], 'title': data['title'], 'duration': data['duration']}

    def playnext(self, ctx):
        if len(self.queue) > 0:
            self.isPlaying = True
            self.ctx = ctx
            self.currentSong = self.queue[0][0]['title']
            url = self.queue[0][0]['source']

            file = discord.FFmpegPCMAudio(url, **ffmpegOptions)
 

            self.musicTime = self.queue[0][0]['duration']
            self.queue.pop(0)
            self.changeLoopTime = True
            self.vc.play(source=file, after=lambda e: self.playnext(ctx))
        else:
            self.isPlaying = False
        
    def prepareArg(self, arg):
        string = " ".join(arg)
        return string
    
    async def playMusic(self, ctx):
        if len(self.queue) > 0:
            self.ctx = ctx
            self.currentSong = self.queue[0][0]['title']
            self.isPlaying = True
            await self.checkVoiceChannel(ctx)

            url = self.queue[0][0]['source']

            file = discord.FFmpegPCMAudio(url, **ffmpegOptions)

            file = discord.PCMVolumeTransformer(file, volume=self.volume)

            self.musicTime = self.queue[0][0]['duration']
            self.queue.pop(0)
            self.vc.play(source=file, after=lambda e: self.playnext(ctx))
            self.changeLoopTime = True
            print("starting checkIsPlaying loop")
            await self.checkIsPlaying.start()
        else:
            self.isPlaying = False

    @commands.command(name="play", aliases= ["p"],  help="Plays from a youtube url")
    async def play(self, ctx, *args):

        url = self.prepareArg(args)
       
        voiceChannel = ctx.author.voice.channel
        if voiceChannel is None:
            await ctx.send("Connect to a voice channel first")
        
        elif self.isPaused:
            self.vc.resume()

        else: 
            song = self.searchyt(url)

        if type(song) == type(True):
            await ctx.send("Could'nt download the song")
        else:
            await ctx.send(f":dvd: {song['title']} added to the queue")
            self.queue.append([song, voiceChannel])
            self.ctx = ctx

            if self.isPlaying == False:
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

    async def leave(self):
        "disconnects the bot from voice"
        if self.vc.is_connected():
            print(f"leaving {self.vc}")
            await self.ctx.send(" :regional_indicator_f: leaving...")
            await self.vc.disconnect(force=True)
            self.checkIsPlaying.cancel()
            self.vc = None
            self.isPlaying = False
            
    @commands.command(name="clear-queue", aliases=['c', 'clearq'], help='Clears the queue')
    async def clear(self, ctx):
        print("Clearing queue...")
        self.queue = []
        await ctx.send(":broom: Music queue cleared")

    @commands.command(name="skip", aliases=["next"], help="skips the current music(if there's no other music it leaves the channel)")
    async def skip(self, ctx):
        if self.vc != None:
            await ctx.send(":fast_forward: Skiping music")
            self.vc.stop()
            if len(self.queue) == 0:
                self.isPlaying = False
                await self.leave()
            else:
                self.changeLoopTime = False
                self.checkIsPlaying.cancel()
                self.checkIsPlaying.restart()
                await asyncio.sleep(1)
                await self.playMusic(ctx)

    @commands.command(name="show-queue", aliases = ["sq", "showq"], help="show the next 10 music in queue")
    async def showQueue(self, ctx):
        string = "```"
        if len(self.queue) == 0:
            await ctx.send(":o: There's nothin in queue")
     
        else:
            for i in range(0, 10):
                try:
                    string += f"{i+1} - " + self.queue[i][0]['title'] + "\n"
                except:
                    break
            string += "```"
            await ctx.send(string)

    @commands.command(name="stop", aliases=["st", "parar"], help="Stops the music and disconnect the bot")
    async def stop(self, ctx):
        if self.vc != None and self.isPlaying:
            self.vc.stop()
            self.queue = []
            await self.leave()

        else:
            await ctx.send("I'm not playing music, bro :slight_frown:")

    @commands.command(name="play-playlist", aliases=["pp", "playp"], help="Plays a playlist from a youtube url")
    async def playPlaylist(self, ctx, *args):
        url = self.prepareArg(args)
        voiceChannel = ctx.author.voice.channel

        GETPLAYLISTSIZEOPTIONS = {
            "quiet": False,
            "ignoreerrors": True,
            "skip_download": True,
            "no_warnings": True,
            "playlistend" : 0,
        }

        ytdlp = yt_dlp.YoutubeDL(GETPLAYLISTSIZEOPTIONS)

        def getPlaylistSize(playlisturl : str) -> int:
            try:
                info = ytdlp.extract_info(playlisturl, download=False)
                return info["playlist_count"]
            except Exception:
                return -1
  
        playlistSize = getPlaylistSize(url)
        print(playlistSize)

        if playlistSize == -1:
            await ctx.send("Could'nt download the playlist")
            return
            
        if voiceChannel is None:
            await ctx.send("Connect to a voice channel first")
        
        elif self.isPaused:
            self.vc.resume()

        else:
            firstSong = self.searchytPlaylist(url)

            if type(firstSong) == type(True):
                await ctx.send("Could'nt download the song")
            else:
                self.queue.append([firstSong, voiceChannel])
                if not self.isPlaying:
                    threadInputMusics = threading.Thread(target=self.inputMusicsInQueue, args=(url, playlistSize, voiceChannel))
                    if __name__ == "cogs.MusicCommand":
                        threadInputMusics.start()
                        await self.playMusic(ctx)
                        threadInputMusics.join()
                        await ctx.send("Playlist added to queue")
                else:
                    self.queue.append([firstSong, voiceChannel])
                    self.inputMusicsInQueue(url, playlistSize, voiceChannel)
                    return
    
    def searchytPlaylist(self, url: str, youtubedlOptions = ytdlFormmatOptions):
        try:
            data = yt_dlp.YoutubeDL(youtubedlOptions).extract_info(url, download=False)['entries'][0]

        except Exception:
            return False
        return {'source': data['url'], 'title': data['title'], 'duration': data['duration']}

    def inputMusicsInQueue(self, playlistURL : str, playlistSize : int, voiceChannel) -> str:
        print("inserting musics in queue")
        for i in range(2, playlistSize):
            ytdlFormmatOptions["playlist_items"] = f"{i}"
            print(f"downloading music {ytdlFormmatOptions['playlist_items']}")
            song = self.searchytPlaylist(playlistURL, ytdlFormmatOptions)
            self.queue.append([song, voiceChannel])

        ytdlFormmatOptions["playlist_items"] = "1"
        return "All musics added to queue"

    @commands.command(name="shuffle", aliases=["sh", "embaralhar"], help="Shuffles the queue")
    async def shuffle(self, ctx) -> None:
        """Shuffles the queue"""
        import random
        random.shuffle(self.queue)
        await ctx.send("Queue shuffled")
            
async def setup(bot):
    await bot.add_cog(MusicCommands(bot))