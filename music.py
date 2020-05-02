import discord
from discord.ext import commands
from discord.utils import get
import spotipy
import time
import youtube_dl

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
        await ctx.send(f"Now connected to {voicechannel}")
    
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

    """@commands.command()
    async def play(self, ctx, url):
        Play a YouTube song
        guild = ctx.message.guild
        voice_client = guild.voice_client
        if voice_client == None:
            voicechannel = ctx.author.voice.channel
            await voicechannel.connect()
        player = await voice_client.create_ytdl(url)
        players[guild.id] = player
        player.start"""



def setup(bot):
    bot.add_cog(music(bot))