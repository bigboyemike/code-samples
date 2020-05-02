import discord
from discord.ext import commands
import spotipy
import time

class spotify(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def connect(self, ctx, voicechannel: discord.VoiceChannel = None):
        """Gets the bot to join a voice channel"""
        if voicechannel == None:
            voicechannel = ctx.author.VoiceState.channel if not voicechannel else voicechannel
        await voicechannel.connect()
        time.sleep(7)
        await ctx.VoiceClient.disconnect()

def setup(bot):
    bot.add_cog(spotify(bot))