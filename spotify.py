import discord
from discord.ext import commands
import spotipy
import time

class spotify(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx):
        """Gets the bot to join a voice channel"""
        voicechannel = ctx.author.voice.channel
        await voicechannel.connect()
        time.sleep(7)
        await ctx.voice_client.disconnect()

def setup(bot):
    bot.add_cog(spotify(bot))