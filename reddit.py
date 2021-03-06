import discord
from discord.ext import commands
from datetime import date
import datetime
import praw
import os


# Creates a function which compresses post grabbing/embed creating in post subcommands (different post sorts)
async def postInfoGrab(ctx, submission):
    # If the post is text, makes variable 'Text' true to then decide if embed should have an image (if self text there is no image, so it stops it from including an image in the embed)
    if submission.is_self == True:
        Text = True
    else:
        Text = False

    # If post is marked nsfw, checks to make sure discord channel is set as nsfw too. Makes sure no one sees any nsfw they would otherwise not want to see
    if submission.over_18 == True and ctx.channel.is_nsfw() == False:
        return await ctx.send('This channel must be marked as NSFW to view NSFW subreddits!')

    # Formatting score & comment count
    upvotes = "{:,}".format(submission.score)
    commentNum = "{:,}".format(submission.num_comments)

    # Creates embed. Pulls all of the post info, from title to author, score, and comment amount
    postEmbed = discord.Embed(title=submission.title, url=f'https://reddit.com{submission.permalink}',
                              color=discord.Color.red(), description=submission.selftext)
    postEmbed.set_author(name=f'{upvotes} upvotes and {commentNum} comments.')
    postEmbed.set_footer(text=f'Posted by {submission.author}')
    # Uses 'Text' variable to decide if to attach image to embed
    if Text == False:
        postEmbed.set_image(url=submission.url)
    return postEmbed


class reddit(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        self.reddit = praw.Reddit(client_id=os.environ['Rclient_id'],
                                  client_secret=os.environ['Rclient_secret'],
                                  user_agent=os.environ['Ruser_agent'],
                                  username=os.environ['Rusername'],
                                  password=os.environ['Rpassword'])

    @commands.group()
    async def post(self, ctx):
        """View a post in a specified subreddit"""
        if ctx.invoked_subcommand is None:
            return await ctx.send(
                "No sort and subreddit were provided. Accepted sorts are hot, new, rising, controversial, and top.")

    # If someone wants to view a post in hot
    @post.command()
    async def hot(self, ctx, subreddit):
        # Defining what sub bot looks through
        subreddit = self.reddit.subreddit(subreddit)
        # Picking out the post to get info from
        for submission in subreddit.hot(limit=3):
            if submission.stickied == True:
                continue
            finalEmbed = await postInfoGrab(ctx, submission)
        return await ctx.send(embed=finalEmbed)

    # If someone wants to view a post in new
    @post.command()
    async def new(self, ctx, subreddit):
        # Defining what sub bot looks through
        subreddit = self.reddit.subreddit(subreddit)
        # Picking out the post to get info from
        for submission in subreddit.new(limit=1):
            finalEmbed = await postInfoGrab(ctx, submission)
        return await ctx.send(embed=finalEmbed)

    # If someone wants to view a post in rising
    @post.command()
    async def rising(self, ctx, subreddit):
        # Defining what sub bot looks through
        subreddit = self.reddit.subreddit(subreddit)
        # Picking out the post to get info from
        for submission in subreddit.rising(limit=1):
            finalEmbed = await postInfoGrab(ctx, submission)
        return await ctx.send(embed=finalEmbed)

    # If someone wants to view a post in controversial
    @post.command()
    async def controversial(self, ctx, subreddit):
        # Defining what sub bot looks through
        subreddit = self.reddit.subreddit(subreddit)
        # Picking out the post to get info from
        for submission in subreddit.controversial(limit=1):
            finalEmbed = await postInfoGrab(ctx, submission)
        return await ctx.send(embed=finalEmbed)

    # If someone wants to view a post in top
    @post.command()
    async def top(self, ctx, subreddit):
        # Defining what sub bot looks through
        subreddit = self.reddit.subreddit(subreddit)
        # Picking out the post to get info from
        for submission in subreddit.top(limit=1):
            finalEmbed = await postInfoGrab(ctx, submission)
        return await ctx.send(embed=finalEmbed)

    @commands.command()
    @commands.is_owner()
    async def redditmsg(self, ctx, user, *, message):
        """Send a reddit message to a user"""
        try:
            # Attempts to send a message to user specified. Includes a subject with author's name and states it was sent via the bot so receivers are aware. Also adds a reaction to let sender know message was successfully sent
            self.reddit.redditor(user).message(f'This is a message sent from {ctx.author} via Mikey#1211', message)
            return await ctx.message.add_reaction(emoji='<:check:688848512103743511>')
        except:
            # If message sending fails, returns error message
            return await ctx.send('There was an error sending the message.')

    @commands.group(aliases=['karma', 'ri'], invoke_without_command=True)
    async def redditinfo(self, ctx, redditor=None):
        """Look at a reddit account's info"""
        # Creates a string version of the user's ID, to be used in the database queries
        user_id = str(ctx.author.id)
        # If no redditor is states, bot searches database to see if user already set their username
        if redditor is None:
            redditU = await self.bot.pg_con.fetch("SELECT reddit_name FROM user_info WHERE user_id = $1", user_id)
            # If no entry for that user is found, send a message explaining how to set a username
            if not redditU:
                return await ctx.send(
                    'No username specified. To store your reddit username use `redditinfo set <username>`')
            # Converts redditor entry from database into a string, which can be understood by Reddit's API (praw)
            redditor = redditU[0][0]

        # Simplifies the redditor, so it's easier to later use for info.
        user = self.reddit.redditor(redditor)

        # Formats karma to include commas. Also calculates total karma.
        totalKarma = "{:,}".format(user.comment_karma + user.link_karma)
        linkKarma = "{:,}".format(user.link_karma)
        commentKarma = "{:,}".format(user.comment_karma)

        # Obtains account creation date and formats to be user-friendly
        createdTime = datetime.datetime.utcfromtimestamp(user.created_utc)
        ct = createdTime.strftime("%b %d, %Y")

        # Creates actual embed. Pulls name and icon, also uses the formatted karma amounts and formatted creation date.
        redditInfoEmbed = discord.Embed(title=user.name, color=discord.Color.red())
        redditInfoEmbed.set_thumbnail(url=user.icon_img)
        redditInfoEmbed.add_field(name='<:karma:702194343724974141> **Karma**',
                                  value=f'**{totalKarma} total:** \n {linkKarma} post \n {commentKarma} comment')
        redditInfoEmbed.set_footer(text=f'Account created on {ct}')
        # Sends embed
        await ctx.send(embed=redditInfoEmbed)

    #Subcommand which allows user to set their reddit username
    @redditinfo.command()
    async def set(self, ctx, username):
        # Creates a string version of the user's ID, to be used in the database queries
        user_id = str(ctx.author.id)
        # Fetches user's entry in the table, if non-existent bot creates one
        user = await self.bot.pg_con.fetch("SELECT * FROM user_info WHERE user_id = $1", user_id)
        # Creates entry for that user
        if not user:
            await self.bot.pg_con.execute("INSERT INTO user_info (user_id) VALUES ($1)", user_id)
        # Updates user entry to new reddit username, one that the user provided
        await self.bot.pg_con.execute("UPDATE user_info SET reddit_name = $1 WHERE user_id = $2", username, user_id)
        # Adds a reaction to user's message to let them know process is successful/completed
        await ctx.message.add_reaction('<:check:688848512103743511>')


def setup(bot):
    bot.add_cog(reddit(bot))
