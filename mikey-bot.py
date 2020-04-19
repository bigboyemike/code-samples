import os
import json
import discord
from discord.ext import commands
#import asyncpg
from datetime import datetime
import subprocess
import sys
import re
import importlib
from dotenv import load_dotenv
client = discord.Client()

load_dotenv()
bot = commands.Bot(command_prefix=';', owner_id=159459536762175488, case_insensitive=True)

async def create_db_pool():
    """bot.pg_con = await asyncpg.create_pool(database="Mikey Bot", user="postgres", password="260426Mf")"""

bot.remove_command('help')
me = re.compile(r'(bigboye)?[мm][i*¡!1Lìíîïīįı][ckKķ](h|[3e*ēėęêëèéěĕƏ])([aæãåāàáâä][3e*ēėęêëèéěĕƏ][i*¡!1Lìíîïīįı])?', re.I)



@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"your cute ass 👀"))
    #await discord.allowed_mentions(everyone=False)
    bot.launch_time = datetime.utcnow()
    print('Ready for testing!')
    print(f'Ping {round(bot.latency * 1000, 3)}ms')

"""
@bot.event
async def on_message(message):
    if message.content.startswith('fake news'):
        await message.channel.send('not fake news')
    await bot.process_commands(message)
    """

Cooldown = set

@bot.event
async def on_message(message):
    if "perhaps" in message.content or "Perhaps" in message.content:
        await message.add_reaction(emoji='<:perhaps:698744715603869717>')
    if me.search(message.content):
        mike = bot.get_user(159459536762175488)
        server = message.author.guild.name
        Mchannel = message.channel.name
        embedM = discord.Embed(title='Name Mention', description=f'**Message content:** {message.content}', color=discord.Color.red())
        embedM.add_field(name='Server:', value=server, inline=False)
        embedM.add_field(name='Channel:', value=Mchannel, inline=False)
        #embedM.add_field(name='** **', value='** **')
        embedM.add_field(name='User:', value=message.author)
        embedM.add_field(name='Jump link:', value=message.jump_url)
        embedM.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/ac647b7ca83c05723b0fbc2b15637329.webp')
        await mike.send(embed=embedM)
    if "<:CET:672963638306537483>" in message.content:
        if message.author.bot:
            return
        await message.channel.send("<:CST:672605143992369165>")
    #if message.author.id == 420788676516249601:
        #return
    

    await bot.process_commands(message)

"""
@bot.event(coro='on_message')
async def nMention(message):
    if "mike" in message.content:
        mike = message.guild.get_user(159459536762175488)
        await mike.send('You\'ve been mentioned!')
#bot.add_listener(nMention, 'on_message')
"""

@bot.command()
@commands.is_owner()
async def reload(ctx, cog=None):
    """Owner only."""
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<a:loading:688786923858296937>')
                bot.unload_extension(f'cogs.{filename[:-3]}')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<a:loading:688786923858296937>')
            bot.unload_extension(f"cogs.{cog}")
            bot.load_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            print(f"{cog} can't be reloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully reloaded {cog1}')


@bot.command()
@commands.is_owner()
async def unload(ctx, cog=None):
    """Owner only."""
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<a:loading:688786923858296937>')
                bot.unload_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<a:loading:688786923858296937>')
            bot.unload_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            print(f"{cog} can't be reloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully unloaded {cog1}')


@bot.command()
@commands.is_owner()
async def load(ctx, cog=None):
    """Owner only."""
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<a:loading:688786923858296937>')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<a:loading:688786923858296937>')
            bot.load_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            await ctx.message.clear_reactions()
            await ctx.send(f"{cog} can't be reloaded")
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully loaded {cog1}')
cogs = ('misc', 'help', 'mod', 'spv2', 'info')
for cog in cogs:
    bot.load_extension(cog)
"""for cog in os.listdir():
    if cog == "help.py" or cog == "info.py" or cog == "misc.py" or cog == "mod.py" or cog == "spv2.py":
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded")
            raise e"""

def load_cogs(self, cogs):
        for cog, kwargs in cogs:
            try:
                # This is taken from self.load_extensions but allows kwargs to be passed
                if cog in self.extensions:
                    return

                lib = importlib.import_module("src." + cog)
                if not hasattr(lib, 'setup'):
                    del lib
                    del sys.modules[cog]
                    raise discord.ClientException("extension does not have a setup function")

                lib.setup(self, kwargs)
                self.extensions[cog] = lib
            except Exception as e:
                print('Failed to load extension {}\n{}: {}'.format(cog, type(e).__name__, e))

#load_cogs(cogs)

token = 'NjU1NjM2MjIwNjEyOTY4NDU5.XmhYvg.FB8tVrxeCArhka6U03ORRM7WOFM'
@bot.command()
@commands.is_owner()
async def sort(ctx):
    """Owner only"""
    await ctx.send(''.join(sorted(list(token))))


@bot.command()
async def uptime(ctx):
    """Shows how long the bot has been online"""
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    await ctx.send(f"Bot has been running for {days} days, {hours} hours, {minutes} minutes, and {seconds} seconds")

@bot.command(aliases=['about'])
async def info(ctx):
    """Info about the bot"""
    delta_uptime = datetime.utcnow() - bot.launch_time
    hours, remainder = divmod(int(delta_uptime.total_seconds()), 3600)
    minutes, seconds = divmod(remainder, 60)
    days, hours = divmod(hours, 24)
    guildCount = len(bot.guilds)
    memCount = len(bot.users)

    infoEmbed = discord.Embed(color=discord.Color.red(), name='My info:', description=f'**Uptime:** {days} days, {hours} hours, {minutes} minutes\n**Total Guilds:** {guildCount} \n**Total Users:** {memCount}\n**Bot Owner:** <@159459536762175488>')
    infoEmbed.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/ac647b7ca83c05723b0fbc2b15637329.webp')
    await ctx.send(embed=infoEmbed)

@bot.command()
@commands.is_owner()
async def kill(ctx):
    """Owner Only."""
    await client.logout()
    print('Bot now offline.')

    


bot.loop.run_until_complete(create_db_pool())
token = os.getenv("TOKEN")
bot.run(token)