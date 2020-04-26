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
    async def aaa(self, ctx):
        
        postInfo = { "title":[],
                    "score":[],
                    "id":[], "url":[],
                    "comms_num": [],
                    "created": [],
                    "body":[],
                    "author":[],
                    "selftext":[]}
        subreddit = self.reddit.subreddit('dankmemes')
        for submission in subreddit.top(limit=1):
            postInfo["title"].append(submission.title)
            postInfo["score"].append(submission.score)
            postInfo["id"].append(submission.id)
            postInfo["url"].append(submission.url)
            postInfo["comms_num"].append(submission.num_comments)
            postInfo["created"].append(submission.created)
            postInfo["body"].append(submission.selftext)
            postInfo["author"].append(submission.author)
            postInfo["selftext"].append(submission.selftext)
            if submission.is_self == True:
                Text = True
            else:
                Text = False

        postEmbed = discord.Embed(title=postInfo["title"], color=discord.Color.red(), description=postInfo["selftext"])
        postEmbed.set_footer(text=f'Posted by {postInfo["author"]} with a score of {postInfo["score"]}. Post has {postInfo["comms_num"]} comments.')
        if Text == False:
            postEmbed.set_image(url=postInfo["url"])
        return await ctx.send(embed=postEmbed)



def setup(bot):
    bot.add_cog(reddit(bot))