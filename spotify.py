import discord
from discord.ext import commands
import spotipy

class spotify(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

def setup(bot):
    bot.add_cog(spotify(bot))