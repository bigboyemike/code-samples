import discord
from datetime import date
from discord.ext import commands
import inspect
from datetime import datetime
import typing

class info(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['ui','user'])
    async def userinfo(self, ctx, *, user: typing.Union[discord.Member, discord.User, int, None]):
        """Get info about a user"""
        user = user or ctx.author
        if isinstance(user, int):
            user = await self.bot.fetch_user(user)
        if user == None:
            user = ctx.author if not user else user
        
        if user == self.bot.user:
            botStatus = 'Yes'
        else:
            botStatus = 'No'

        createdTime = user.created_at
        ct = createdTime.strftime("%b %d, %Y")
        for member in ctx.guild.members:
            if member.name == user.name:
                joinedTime = user.joined_at
                jt = joinedTime.strftime("%b %d, %Y")
                inGuild = True

        roles = []
        for role in user.roles:
            roles.append(role)

        statusE = {
            "online": "<:online:686059993006342217>",
            "idle": "<:away:686060018034016286>",
            "dnd": "<:dnd:686060039190216713>",
            "offline": "<:offline:686060058118717453>"
        }

        try:
            embed = discord.Embed(color=user.color, title=f'{user.display_name}\'s Info', footer=f'Requested by {ctx.author}')
            embed.set_author(name=f'{user}', icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='**ID:**', value=user.id, inline=True)
            embed.add_field(name='**Is this user a bot?**', value=botStatus, inline=True)
            embed.add_field(name='**User\'s roles:**', value=" ".join([role.mention for role in roles if role.id != ctx.guild.id]), inline=False) 
            embed.add_field(name='**User\'s Status:**', value=statusE[str(user.web_status)] + 'Web Status' + '\n' + statusE[str(user.mobile_status)] + 'Mobile Status' + '\n' + statusE[str(user.desktop_status)] + 'Desktop Status', inline=False)
            embed.add_field(name='**Account created:**', value=ct, inline=True)
            if inGuild == True:
                embed.add_field(name='**Joined server:**', value=jt, inline=True)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        except discord.errors.HTTPException:
            embed = discord.Embed(color=user.color, title=f'{user.display_name}\'s Info', footer=f'Requested by {ctx.author}')
            embed.set_author(name=f'{user}', icon_url=user.avatar_url)
            embed.set_thumbnail(url=user.avatar_url)
            embed.set_footer(text=f'Requested by {ctx.author}', icon_url=ctx.author.avatar_url)
            embed.add_field(name='**ID:**', value=user.id, inline=True)
            embed.add_field(name='**Is this user a bot?**', value=botStatus, inline=True)
            embed.add_field(name='**User\'s roles:**', value='User has no roles', inline=False) 
            embed.add_field(name='**User\'s Status:**', value=statusE[str(user.web_status)] + 'Web Status' + '\n' + statusE[str(user.mobile_status)] + 'Mobile Status' + '\n' + statusE[str(user.desktop_status)] + 'Desktop Status', inline=False)
            embed.add_field(name='**Account created:**', value=ct, inline=True)
            if inGuild == True:
                embed.add_field(name='**Joined server:**', value=jt, inline=True)
            embed.timestamp = ctx.message.created_at
            await ctx.send(embed=embed)
        except:
            await ctx.send('There was an error fetching user\'s info')

    @commands.command(aliases=['gi','guild'])
    async def guildinfo(self, ctx):
        """Get info about the server (WIP)"""

        createdTime = ctx.guild.created_at
        ct = createdTime.strftime("%b %d, %Y")

        emojiList = []
        for e in ctx.guild.emojis:
            if e.animated == False:
                emojiList.append(e)
        emojiNum = len(emojiList)
        channelNum = len(ctx.guild.channels)
        textChannelNum = len(ctx.guild.text_channels)
        voiceChannelNum = len(ctx.guild.voice_channels)
        if textChannelNum == 1:
            sOrNotT = 'channel'
        else:
            sOrNotT = 'channels'
        if voiceChannelNum == 1:
            sOrNotV = 'channel'
        else:
            sOrNotV = 'channels'

        guildEmbed = discord.Embed(color=ctx.author.color, title=f'{ctx.guild.name} - This command is a work in progress!')
        guildEmbed.set_thumbnail(url=ctx.guild.icon_url)
        guildEmbed.add_field(name='**General info:**', value=f'**Owner:** {ctx.guild.owner.mention}\n**Created on:** {ct}\n**Member count:** {ctx.guild.member_count}\n**Emoji count:** {emojiNum}/{ctx.guild.emoji_limit}\n**Total channels:** {channelNum} ({textChannelNum} text {sOrNotT}, {voiceChannelNum} voice {sOrNotV})')
        await ctx.send(embed=guildEmbed)

        

        
        
def setup(bot):
    bot.add_cog(info(bot))