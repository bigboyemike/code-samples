import discord
from discord.ext import commands
from discord.utils import get
import spotipy
import time
import youtube_dl
import os
import lavalink
from discord import utils
from discord import Embed

class music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot
        self.bot.music = lavalink.Client(self.bot.user.id)
        self.bot.music.add_node('localhost', 7000, 'testing', 'na', 'music-node')
        self.bot.add_listener(self.bot.music.voice_update_handler, 'on_socket_response')
        self.bot.music.add_event_hook(self.track_hook)

    @commands.command(name='join')
    async def join(self, ctx):
        print('join command worked')
        member = utils.find(lambda m: m.id == ctx.author.id, ctx.guild.members)
        if member is not None and member.voice is not None:
            vc = member.voice.channel
            player = self.bot.music.player_manager.create(ctx.guild.id, endpoint=str(ctx.guild.region))
            if not player.is_connected:
                player.store('channel', ctx.channel.id)
                await self.connect_to(ctx.guild.id, str(vc.id))

    @commands.command(name='play')
    async def play(self, ctx, *, query):
        try:
            player = self.bot.music.player_manager.get(ctx.guild.id)
            query = f'ytsearch:{query}'
            results = await player.node.get_tracks(query)
            tracks = results['tracks'][0:10]
            i = 0
            query_result = ''
            for track in tracks:
                i = i + 1
                query_result = query_result + f'{i}) {track["info"]["title"]} - {track["info"]["uri"]}\n'
            embed = Embed()
            embed.description = query_result

            await ctx.channel.send(embed=embed)

            def check(m):
                return m.author.id == ctx.author.id
      
            response = await self.bot.wait_for('message', check=check)
            track = tracks[int(response.content)-1]

            player.add(requester=ctx.author.id, track=track)
            if not player.is_playing:
                await player.play()

        except Exception as error:
            print(error)
  
    async def track_hook(self, event):
        if isinstance(event, lavalink.events.QueueEndEvent):
            guild_id = int(event.player.guild_id)
            await self.connect_to(guild_id, None)
      
    async def connect_to(self, guild_id: int, channel_id: str):
        ws = self.bot._connection._get_websocket(guild_id)
        await ws.voice_state(str(guild_id), channel_id)
    
    """@commands.command()
    async def connect(self, ctx):
        Gets the bot to join your voice channel
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(voicechannel)
        else:
            voice = await voicechannel.connect()
        await ctx.send(f"Connected to {voicechannel}")
    
    @commands.command()
    async def disconnect(self,ctx):    
        Makes the bot leave the voice channel
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            return await ctx.send(f"Disconnected from {voicechannel}")
        else:
            return await ctx.send("Bot isn't in a voice channel!")

    @commands.command()
    async def play(self, ctx, url: str):
        Play a YouTube song
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        player = await voice.create_ytdl_player(url)
        player.start
        
        ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
        }
        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])
        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                voice.play(discord.FFmpegAudio(file), args=file, executable='ffmpeg', after=lambda e: print("song finished playing"))
            
        


        songPresent = os.path.isfile("song.mp3")
        try:
            if songPresent:
                os.remove("song.mp3")
        except PermissionError:
            return await ctx.send("have some patience dumbass there's a song already playing")
        
        await ctx.send("Preparing song...")
        ydl_opts = {
                    'format': 'bestaudio/best',
                    'postprocessors': [{
                        'key': 'FFmpegExtractAudio',
                        'preferredcodec': 'mp3',
                        'preferredquality': '192',
                    }],
        }

        with youtube_dl.YoutubeDL(ydl_opts) as ydl:
            ydl.download([url])

        for file in os.listdir("./"):
            if file.endswith(".mp3"):
                name = file
                os.rename(file, "song.mp3")
        
        voice.play(discord.FFmpegPCMAudio("song.mp3"), after=lambda e: print("song finished playing"))
        voice.source = discord.PCMVolumeTransformer(voice.source)
        voice.source.volume

        newName = name.rsplit("-", 2)
        await ctx.send(f"Now playing {newName}")"""



def setup(bot):
    bot.add_cog(music(bot))