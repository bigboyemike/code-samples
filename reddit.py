import discord
from discord.ext import commands
from datetime import date
import praw
class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id='AEvZJBsDYQtxyg',
                        client_secret='fijOdLQH2JpC8y8gxPEt8r5TVoQ',
                        user_agent='Mikey Bot by u/TheHiMaster. Integrated with Mikey#1211 on Discord.',
                        username='Mikey_Bot',
                        password='260426Mf')
    
    @commands.command()
    async def toppost(self, ctx, sub):
        """View the post in a sub"""
        #Defining what sub bot looks through
        subreddit = self.reddit.subreddit(sub)
        #If the sort doesn't equal one of the valid sorts, a message is returned saying it's not valid
        """if sort == 'hot' or 'top' or 'rising' or 'new' or 'best' or 'controversial':
            pass
        else:
            return await ctx.send('That sort is not valid!')"""
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

            #Formatting score & comment count
            upvotes = "{:,}".format(submission.score)
            commentNum = "{:,}".format(submission.num_comments)
            
            #Creates embed. Pulls all of the post info, from title to author, score, and comment amount
            postEmbed = discord.Embed(title=f'[{submission.title}]({submission.permalink})', color=discord.Color.red(), description=submission.selftext)
            postEmbed.set_author(name=f'Posted by u/{submission.author}. {upvotes} upvotes, {commentNum} comments.')
            postEmbed.set_footer(text=f'Post taken from r/{sub}')
            #Uses 'Text' variable to decide if to attach image to embed
            if Text == False:
                postEmbed.set_image(url=submission.url)
            #Sends embed
            return await ctx.send(embed=postEmbed)

    @commands.command()
    async def redditmsg(self, ctx, user, *, message):
        """Send a reddit message to a user"""
        self.reddit.redditor(user).message(f'This is a message sent from {ctx.author} via Mikey#1211', message)
        return await message.add_reaction(emoji='<:check:688848512103743511>')
        """except:
            return await ctx.send('There was an error sending the message. Check to make sure you spelled the username correctly.')"""




def setup(bot):
    bot.add_cog(reddit(bot))