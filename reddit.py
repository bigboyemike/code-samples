import discord
from discord.ext import commands
from datetime import date
import praw
import format

class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='iRtVWc-sNNcr0g',
                        client_secret='wfKJrXw484m5F5wNRI-p2n6gBLM',
                        user_agent='Mikey Bot by u/TheHiMaster',
                        username='TheHiMaster',
                        password='260426Mf')
    
    @commands.command()
    async def aaa(self, ctx, sub):
        """View the top post in a sub"""
        #Defining what sub bot looks through
        subreddit = self.reddit.subreddit(sub)
        #Picking out the post to get info from
        for submission in subreddit.top(limit=1):
            #If the post is text, makes variable 'Text' true to then decide if embed should have an image
            if submission.is_self == True:
                Text = True
            else:
                Text = False
            #If post is marked nsfw, checks to make sure discord channel is set as nsfw too. Makes sure no one sees any nsfw they would otherwise not want to see
            if submission.over_18 == True and ctx.channel.is_nsfw() == False:
                return await ctx.send('This channel must be marked as NSFW to view NSFW subreddits!')

            upvotes = "{:,}".format(submission.score)
            commentNum = "{:,}".format(submission.num_comments)
            #Creates embed. Pulls all of the post info, from title to author, score, and comment amount
            postEmbed = discord.Embed(title=submission.title, color=discord.Color.red(), description=submission.selftext)
            postEmbed.set_footer(text=f'Posted by {submission.author} with {upvotes}upvotes. Post has {commentNum} comments.')
            #Uses 'Text' variable to decide if to attach image to embed
            if Text == False:
                postEmbed.set_image(url=submission.url)
            #Sends embed
            return await ctx.send(embed=postEmbed)



def setup(bot):
    bot.add_cog(reddit(bot))