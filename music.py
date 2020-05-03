import discord
from discord.ext import commands
from discord.utils import get
import spotipy
import time
import youtube_dl
import os

class music(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        """Gets the bot to join your voice channel"""
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.move_to(voicechannel)
        else:
            voice = await voicechannel.connect()
        await ctx.send(f"Connected to {voicechannel}")
    
    @commands.command()
    async def disconnect(self,ctx):    
        """Makes the bot leave the voice channel"""
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        if voice and voice.is_connected():
            await voice.disconnect()
            return await ctx.send(f"Disconnected from {voicechannel}")
        else:
            return await ctx.send("Bot isn't in a voice channel!")

    @commands.command()
    async def play(self, ctx, url: str):
        """Play a YouTube song"""
        voicechannel = ctx.author.voice.channel
        voice = get(self.bot.voice_clients, guild=ctx.guild)
        """player = await voice.create_ytdl_player(url)
        player.start"""
        
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
        await ctx.send(f"Now playing {newName}")



def setup(bot):
    bot.add_cog(music(bot))