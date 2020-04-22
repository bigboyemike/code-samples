import discord
from discord.ext import commands
from datetime import date
import praw

class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    reddit = praw.Reddit(client_id='iRtVWc-sNNcr0g',
                     client_secret='	wfKJrXw484m5F5wNRI-p2n6gBLM',
                     password='260426Mf',
                     user_agent='Mikey Bot by u/TheHiMaster',
                     username='TheHiMaster')
    #print(reddit.auth.url(['identity'], '...', 'permanent'))

    @commands.command()
    async def subhot(self, ctx, sub):
        """Get a random post in hot from a specific subreddit"""
        #for submission in reddit.subreddit(sub).hot(limit=1):
            #await ctx.send(submission.title)

def setup(bot):
    bot.add_cog(reddit(bot))