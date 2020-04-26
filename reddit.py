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

    postInfo = { "title":[],
                "score":[],
                "id":[], "url":[],
                "comms_num": [],
                "created": [],
                "body":[]}
    
    @commands.command()
    async def aaa(self, ctx, sub):
        
        postInfo = { "title":[],
                    "score":[],
                    "id":[], "url":[],
                    "comms_num": [],
                    "created": [],
                    "body":[],
                    "author":[],
                    "selftext":[]}
        subreddit = self.reddit.subreddit(sub)
        for submission in subreddit.top(limit=1):
            if submission.is_self == True:
                Text = True
            else:
                Text = False
            if submission.over_18 == True and ctx.channel.is_nsfw() == False:
                return await ctx.send('This channel must be marked as NSFW to view NSFW subreddits!')


            postEmbed = discord.Embed(title=submission.title, color=discord.Color.red(), description=submission.selftext)
            postEmbed.set_footer(text=f'Posted by {submission.author} with a score of {submission.score}. Post has {submission.num_comments} comments.')
            if Text == False:
                postEmbed.set_image(url=submission.url)
            return await ctx.send(embed=postEmbed)



def setup(bot):
    bot.add_cog(reddit(bot))