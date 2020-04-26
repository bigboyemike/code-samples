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
    async def post(self, ctx, sort, sub):
        """View a post in a sub with a sort of choice"""
        #Defining what sub bot looks through
        subreddit = self.reddit.subreddit(sub)
        #If the sort doesn't equal one of the valid sorts, a message is returned saying it's not valid
        if sort == 'hot' or 'top' or 'rising' or 'new' or 'best' or 'controversial':
            pass
        else:
            return await ctx.send('That sort is not valid!')
        #Picking out the post to get info from
        for submission in subreddit.sort(limit=1):
            #If the post is text, makes variable 'Text' true to then decide if embed should have an image
            if submission.is_self == True:
                Text = True
            else:
                Text = False
            #If post is marked nsfw, checks to make sure discord channel is set as nsfw too. Makes sure no one sees any nsfw they would otherwise not want to see
            if submission.over_18 == True and ctx.channel.is_nsfw() == False:
                return await ctx.send('This channel must be marked as NSFW to view NSFW subreddits!')

            #Formatting score & comment count
            upvotes = "{:,}".format(submission.score)
            commentNum = "{:,}".format(submission.num_comments)
            
            #Creates embed. Pulls all of the post info, from title to author, score, and comment amount
            postEmbed = discord.Embed(title=submission.title, color=discord.Color.red(), description=submission.selftext)
            postEmbed.set_author(name=f'Posted by {submission.author}. {upvotes} upvotes, {commentNum} comments.')
            postEmbed.set_footer(text=f'Post taken from r/{sub} and filtered by {sort}')
            #Uses 'Text' variable to decide if to attach image to embed
            if Text == False:
                postEmbed.set_image(url=submission.url)
            #Sends embed
            return await ctx.send(embed=postEmbed)



def setup(bot):
    bot.add_cog(reddit(bot))