import os
import json
import discord
from discord.ext import commands
#import asyncpg
from datetime import datetime
import random
import psutil
import inspect
import subprocess
import sys
import queue
import threading, time, random
import psutil
from discord import Spotify
from datetime import timedelta
from string import Template
client = discord.Client()

def bar_make(value: int, gap: int, fill_char: str = '⚪', empty_char: str = '─', point_mode: bool = True, length: int = 25):
        bar = ''

        percentage = (value/gap) * length

        if point_mode:
            for i in range(0, length+1):
                if i == round(percentage):
                    bar += fill_char
                else:
                    bar += empty_char
            return bar

        for i in range(0, length+1):
            if i <= percentage:
                bar += fill_char
            else:
                bar += empty_char
        return bar

class DeltaTemplate(Template):
    delimiter = "%"

def strfdelta(tdelta, fmt):
    d = {"D": tdelta.days}
    hours, rem = divmod(tdelta.seconds, 3600)
    minutes, seconds = divmod(rem, 60)
    d["H"] = '{:02d}'.format(hours)
    d["M"] = '{:02d}'.format(minutes)
    d["S"] = '{:02d}'.format(seconds)
    t = DeltaTemplate(fmt)
    return t.substitute(**d)
class misc(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command(aliases=['cf'])
    async def coinflip(self, ctx):
        """Flips a virtual coin. 50/50 chance to land on either heads or tails"""
        result = random.randint(1,2)
        if (result == 1):
            await ctx.send('The coin landed on **heads**')
        else:
            await ctx.send('The coin landed on **tails**')

    @commands.command()
    async def ping(self, ctx):
        """Pings the bot to find latency"""
        embed = discord.Embed(title=' ',
                            description=f'**Pong! ** :ping_pong:\n *Latency: {round(self.bot.latency * 1000, 3)}ms*',
                            color=0x000000)
        await ctx.send(embed=embed)
    
    @commands.command()
    async def echo(self, ctx, channel: discord.TextChannel, *, message):
        """Echo a message to the specified channel"""
        try:
            if "@everyone" in message:
                await ctx.send('no')
                return
            if "@here" in message:
                await ctx.send('no')
                return
            await channel.send(message)
            await ctx.message.add_reaction('<:check:688848512103743511>')
            time.sleep(2)
            await ctx.message.delete()
        except:
            await ctx.send('Please specify a valid channel')
            await ctx.message.add_reaction(':x:')

    @commands.command()
    async def say(self,ctx, *, message):
        """Make the bot say something"""
        if "@everyone" in message:
            await ctx.send('no')
            return
        if "@here" in message:
            await ctx.send('no')
            return
        await ctx.message.delete()
        await ctx.send(message)

    @commands.command(aliases=['av','pfp', 'profilepic', 'profilepicture'])
    async def avatar(self, ctx, member: discord.Member = None):
        """Return's a specified user's avatar"""
        try:
            member = ctx.author if not member else member
        except:
            return ctx.send('There was an error finding that user')
        
        embed = discord.Embed()
        embed.set_image(url=member.avatar_url)
        await ctx.send(embed=embed)

    @commands.command()
    async def spam(self, ctx, *, message):
        """Spams a message over and over"""
        if "@everyone" in message:
            await ctx.send('no')
            return
        if "@here" in message:
            await ctx.send('no')
            return
        try:
            await ctx.send(message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ' + message + ' ')
        except:
            await ctx.send('Message is too long to send')

    @commands.command(aliases=['meow', 'catto'])
    async def cat(self, ctx):
        """Sends a random cat"""
        import aiohttp
        session = aiohttp.ClientSession()
        async with session.get('https://aws.random.cat/meow') as response:
            data = await response.json()
            embed = discord.Embed(title='Meow! - Showing a random cat', color=ctx.author.color)
            embed.set_image(url=data['file'])
            embed.set_footer(text='Powered by https://aws.random.cat')
            await ctx.send(embed=embed)
        await session.close()

    @commands.command(aliases=['doggo', 'woof', 'bark'])
    async def dog(self, ctx):
        """Sends a random dog"""
        import aiohttp
        session = aiohttp.ClientSession()
        async with session.get('https://random.dog/woof.json') as response:
            data = await response.json()
            embed = discord.Embed(title='Woof! - Showing a random dog', color=ctx.author.color)
            embed.set_image(url=data['url'])
            embed.set_footer(text='Powered by https://random.dog')
            await ctx.send(embed=embed)
        await session.close()

    @commands.command(aliases=['hl'])
    async def howlong(self, ctx, member: discord.Member =None):
        """Shows how long you've been in the server"""
        member = ctx.author if not member else member
        joinedTime = member.joined_at
        jt = joinedTime.strftime("%A, %B %d, %Y")
        jd = joinedTime.strftime("%I:%M")
        Htime = joinedTime.strftime("%H")
        if int(Htime) > 12:
            AorP = 'PM'
        else:
            AorP = 'AM'
        await ctx.send(f'You\'ve been in this server since {jd} {AorP} UTC on {jt}')

    @commands.command()
    async def ram(self, ctx):
        """The bot's ram"""
        embed = discord.Embed(title='ram')
        embed.set_image(url='https://cdn.britannica.com/s:700x500/92/80592-050-86EF29F3/Mouflon-ram.jpg')
        await ctx.send(embed=embed)
    
    @commands.command(aliases=['s','spot'])
    async def spotify(self, ctx, member: discord.Member = None):
        """Get a user's spotify song"""
        try:
            member = ctx.author if not member else member
        except:
            return ctx.send('There was an error finding that user')

        for activity in member.activities:
            if isinstance(activity, Spotify):
            #if member.ActivityType == "Listening"
                spotifyEmbed = discord.Embed(color=0x1DB954, name=f'{member.display_name}\'s Spotify Info:', icon_url='https://www.freepnglogos.com/uploads/spotify-logo-png/file-spotify-logo-png-4.png')
                spotifyEmbed.set_author(name=f'{member.display_name}\'s Spotify:', icon_url='https://i.imgur.com/rZT1mFe.gif')
                spotifyEmbed.add_field(name='**Song:**', value=f'{activity.title} - [**Link**](https://open.spotify.com/track/{activity.track_id})', inline=True)
                artistlist = ', '.join(activity.artists)
                spotifyEmbed.add_field(name='**Artist(s):**', value=artistlist, inline=True)
                spotifyEmbed.add_field(name='**Album:**', value=activity.album, inline=True)
                songPlayedS = (datetime.utcnow() - activity.start).seconds
                songDurationS = activity.duration.seconds
                songDuration = strfdelta(activity.duration, "%M:%S")
                songPlayedT = (datetime.utcnow() - activity.start)
                songPlayed = strfdelta(songPlayedT, "%M:%S")
                progress_bar = bar_make(songPlayedS, songDurationS, '⬤', '─', True, 25)
                if str(member.mobile_status) != "offline":
                    spotifyEmbed.add_field(name='**Song Progress:**', value=progress_bar)
                else:
                    spotifyEmbed.add_field(name='**Song Progress:**', value=f'`{songPlayed}` {progress_bar} `{songDuration}`', inline=False)
                #spotifyEmbed.add_field(name='**Song Link:**', value=f'{activity.artist}')
                spotifyEmbed.set_thumbnail(url=activity.album_cover_url)
                return await ctx.send(embed=spotifyEmbed)
            else:
                await ctx.send(member.ActivityType)
                return await ctx.send("That user is not listening to Spotify!")

    @commands.command()
    async def owo(self, ctx, *, message):
        """Owoify a message"""
        owoMessageA = message.replace("r", "w")
        owoMessageB = owoMessageA.replace("l", "w")
        owoMessageC = owoMessageB.replace("nn", "nny")
        owoMessageD = owoMessageC.replace("ee", "e")
        owoMessageE = owoMessageD.replace("ove", "uv")
        await ctx.send(owoMessageE)

    @commands.command()
    async def invite(self, ctx):
        """Sends the bot's invite"""
        inviteEmbed = discord.Embed(description='[**Link to invite bot**](https://discordapp.com/api/oauth2/authorize?client_id=655636220612968459&permissions=2147483639&scope=bot)', color=discord.Color.red())
        inviteEmbed.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/ac647b7ca83c05723b0fbc2b15637329.webp')
        inviteEmbed.add_field(name='** **', value='** **')
        await ctx.send(embed=inviteEmbed)
    
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error = getattr(error, 'original', error)
        if isinstance(error, commands.CommandNotFound):
            return
        if isinstance(error, commands.CheckFailure):
            #await ctx.send("You do not have permission to use this command.")
            return
        if isinstance(error, commands.MissingPermissions):
            missing = [perm.replace('_', ' ').replace('guild', 'server').title() for perm in error.missing_perms]
            if len(missing) > 2:
                fmt = '{}, and {}'.format("**, **".join(missing[:-1]), missing[-1])
            else:
                fmt = ' and '.join(missing)
            _message = 'You need the **{}** permission(s) to use this command.'.format(fmt)
            await ctx.send(_message)
            return
        if discord.ext.commands.errors.BadArgument:
            await ctx.send(error)
            raise error
        else:
            await ctx.send('There was an error')


def setup(bot):
    bot.add_cog(misc(bot))