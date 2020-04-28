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
    
    @commands.command(aliases=['toppost'])
    async def top(self, ctx, sub):
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
            postEmbed = discord.Embed(title=submission.title, url=f'https://reddit.com{submission.permalink}', color=discord.Color.red(), description=submission.selftext)
            postEmbed.set_author(name=f'{upvotes} upvotes, {commentNum} comments.')
            postEmbed.set_footer(text=f'Posted by {submission.author}')
            #Uses 'Text' variable to decide if to attach image to embed
            if Text == False:
                postEmbed.set_image(url=submission.url)
            #Sends embed
            return await ctx.send(embed=postEmbed)

    @commands.command()
    @commands.is_owner()
    async def redditmsg(self, ctx, user, *, message):
        """Send a reddit message to a user"""
        try:
            self.reddit.redditor(user).message(f'This is a message sent from {ctx.author} via Mikey#1211', message)
            return await ctx.message.add_reaction(emoji='<:check:688848512103743511>')
        except:
            return await ctx.send('There was an error sending the message.')

    @commands.command(aliases=['karma','ri'])
    async def redditinfo(self, ctx, redditor):
        """Look at a reddit account's info"""
        user = self.reddit.redditor(redditor)
        totalKarma = "{:,}".format(user.comment_karma+user.link_karma)
        linkKarma = "{:,}".format(user.link_karma)
        commentKarma = "{:,}".format(user.comment_karma)
        redditInfoEmbed = discord.Embed(title=user.name, color=discord.Color.red())
        redditInfoEmbed.set_thumbnail(url=user.icon_img)
        redditInfoEmbed.add_field(name='<:karma:702194343724974141> **Karma**', value=f'{totalKarma} total \n {linkKarma} post \n {commentKarma} comment')
        await ctx.send(embed=redditInfoEmbed)




def setup(bot):
    bot.add_cog(reddit(bot))