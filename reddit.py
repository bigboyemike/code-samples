import discord
from discord.ext import commands
from datetime import date
import praw

class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='iRtVWc-sNNcr0g',
                        client_secret='wfKJrXw484m5F5wNRI-p2n6gBLM',
                        user_agent='Mikey Bot by u/TheHiMaster',
                        username='TheHiMaster',
                        password='260426Mf')

    @commands.command()
    async def aaa(self, ctx):
        subreddit = self.reddit.subreddit('dankmemes')
        top_subreddit = subreddit.top(limit=2)
        return await ctx.send(top_subreddit)


def setup(bot):
    bot.add_cog(reddit(bot))