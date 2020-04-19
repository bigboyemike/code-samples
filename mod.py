import discord
from datetime import date
from discord.ext import commands
import inspect
    
class mod(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot



    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearbot(self, ctx, amount: int):
        """Clear bot messages. [;clearbot {amount}]"""
        botmsgs = []
        await ctx.message.delete()
        async for msg in ctx.channel.history():
            if msg.author.bot:
                botmsgs.append(msg)
            if len(botmsgs) == amount:
                break
        await ctx.channel.delete_messages(botmsgs)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clear(self, ctx, amount: int):
        """Clear messages. [;clear {amount}]"""
        await ctx.message.delete()
        await ctx.channel.purge(limit=amount)

    @commands.command()
    @commands.has_permissions(manage_messages=True)
    async def clearuser(self, ctx, member: discord.Member, amount = int):
        """Clear a specific user's messages. [;clearuser {user} {amount}]"""
        usermsgs = []
        await ctx.message.delete()
        async for msg in ctx.channel.history():
            if msg.author == member:
                usermsgs.append(msg)
            if len(usermsgs) == amount:
                break
        await ctx.channel.delete_messages(usermsgs)

    @commands.command()
    @commands.has_permissions(kick_members=True)
    async def kick(self, ctx, member: discord.Member, *, reason=None):
        """Kicks a specified user. [;kick {user} {optional reason}]"""
        try:
            server = ctx.author.guild.name
            await member.send(f'You\'ve been kicked from **{server}** for: **{reason}**.')
            await member.kick(reason=reason)
            await ctx.message.delete()
            await ctx.send(f'{member} has been successfully kicked.')
        except:
            await ctx.send(f'There was an error kicking {member}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def ban(self, ctx, member: discord.Member, *, reason=None):
        """Bans a specified user. [;ban {user} {optional reason}]"""
        try:
            server = ctx.author.guild.name
            await member.send(f'You\'ve been banned from **{server}** for: **{reason}**.')
            await member.ban(reason=reason)
            await ctx.message.delete()
            await ctx.send(f'{member} has been successfully banned.')
        except:
            await ctx.send(f'There was an error banning {member}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def banid(self, ctx, userid):
        """Bans a specified user. [;ban {user} {optional reason}]"""
        try:
            user = client.fetch_user(id)
            #server = ctx.author.guild.name
            #await member.send(f'You\'ve been banned from **{server}** for: **{reason}**.')
            await user.ban()
            await ctx.message.delete()
            await ctx.send(f'{user} has been successfully banned.')
        except:
            await ctx.send(f'There was an error banning {userid}')

    @commands.command()
    @commands.has_permissions(ban_members=True)
    async def unban(self, ctx, userID: int):
        """Unbans a specified user. [;unban {user} {optional reason}]"""
        try:
            bannedUser = ctx.bot.get_user(userID)
            await ctx.guild.unban(bannedUser)
            await ctx.message.delete()
            await ctx.send(f'{bannedUser} has been successfully unbanned.')
            server = ctx.author.guild.name
            await bannedUser.send(f'You\'ve been unbanned from **{server}**.')
        except:
            await ctx.send(f'There was an error unbanning {bannedUser}')

    @commands.command()
    @commands.has_permissions(manage_nicknames=True)
    async def nick(self, ctx, member: discord.Member, *, nickname):
        """Change a user's nickname. [;nick {user} {nickname}]"""
        try:
                nickname = None if not nickname else nickname
        except:
                await ctx.send('There was an error')
        try:    
            await member.edit(nick=nickname)
            await ctx.send(f'{member.name}\'s nickname was successfully changed to `{nickname}`')
        except:
            await ctx.send(f'There was an error changing {member.name}\'s nickname')

    
    
    

    """
    channel = ctx.message.channel
        messages = []
        async for message in client.logs_from(channel, limit=int(amount) + 1):
            messages.append(message)
        await client.delete_messages(messages)
    """

def setup(bot):
    bot.add_cog(mod(bot))