import os
import json
import discord
from discord.ext import commands
import asyncpg
from datetime import datetime
import subprocess
import sys
import re
import importlib
#from dotenv import load_dotenv
client = discord.Client()

#load_dotenv()



async def create_db_pool():
    bot.pg_con = await asyncpg.create_pool(database="mikey", user="postgres", password="260426Mf")

bot.remove_command('help')
me = re.compile(r'(bigboye)?[мm][i*¡!1Lìíîïīįı][ckKķ](h|[3e*ēėęêëèéěĕƏ])([aæãåāàáâä4][3e*ēėęêëèéěĕƏ][i*¡!1Lìíîïīįı])?', re.I)
sarah = re.compile(r'((h|ph|f)r([3e*ēėęêëèéěĕƏ]n|[o0][мm])c(h|ph|f)|[sc][aæãåāàáâä4]r[aæãåāàáâä4]+(h|ph|f)|limes)', re.I)


bot = commands.Bot(command_prefix=';', owner_id=159459536762175488, case_insensitive=True)

@bot.event
async def on_ready():
    await bot.change_presence(status=discord.Status.online, activity=discord.Activity(type=discord.ActivityType.watching, name=f"your cute ass 👀"))
    #await discord.allowed_mentions(everyone=False)
    bot.launch_time = datetime.utcnow()
    print('Ready for testing!')
    print(f'Ping {round(bot.latency * 1000, 3)}ms')


cogs = ('misc', 'help', 'mod', 'spv2', 'info', 'reddit')
for cog in cogs:
    bot.load_extension(cog)

Cooldown = set

@bot.event
async def on_message(message):
    if "perhaps" in message.content or "Perhaps" in message.content:
        await message.add_reaction(emoji='<:perhaps:702344890746535997>')
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
        embedM.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/7d07871355cfadeb850fc10f63520e7d.webp')
        await mike.send(embed=embedM)
    if "<:CET:672963638306537483>" in message.content:
        if message.author.bot:
            return
        await message.channel.send("<:CST:672605143992369165>")
    if sarah.search(message.content):  
        french = bot.get_user(420788676516249601)
        server = message.author.guild.name
        Mchannel = message.channel.name
        embedM = discord.Embed(title='Name Mention', description=f'**Message content:** {message.content}', color=discord.Color.red())
        embedM.add_field(name='Server:', value=server, inline=False)
        embedM.add_field(name='Channel:', value=Mchannel, inline=False)
        #embedM.add_field(name='** **', value='** **')
        embedM.add_field(name='User:', value=message.author)
        embedM.add_field(name='Jump link:', value=message.jump_url)
        embedM.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/ac647b7ca83c05723b0fbc2b15637329.webp')
        await french.send(embed=embedM)
    #if message.author.id == 420788676516249601:
        #return
    

    await bot.process_commands(message)

bot.load_extension('jishaku')

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

    infoEmbed = discord.Embed(color=discord.Color.red(), name='My info:', description=f'**Uptime:** {days} days, {hours} hours, {minutes} minutes\n**Total Guilds:** {guildCount} \n**Total Users:** {memCount}\n**Total Emojis:** {len(bot.emojis)}\n **Cached Messages:** {len(bot.cached_messages)}\n **Bot Owner:** <@159459536762175488>')
    infoEmbed.set_footer(text='Mikey#1211', icon_url='https://cdn.discordapp.com/avatars/655636220612968459/ac647b7ca83c05723b0fbc2b15637329.webp')
    await ctx.send(embed=infoEmbed)

@bot.command()
@commands.is_owner()
async def kill(ctx):
    """Kill the bot"""
    await client.logout()
    print('Bot now offline.')

@bot.command(hidden=True)
@commands.is_owner()
async def unload(ctx, cog=None):
    cog = cog.lower()
    cog = cog.capitalize()
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<:loading:667529420013305857>')
                bot.unload_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<:loading:667529420013305857>')
            bot.unload_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            print(f"{cog} can't be unloaded")
            await ctx.message.clear_reactions()
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f"Successfully unloaded {cog1}")


@bot.command(hidden=True)
@commands.is_owner()
async def load(ctx, cog=None):
    cog = cog.lower()
    cog = cog.capitalize()
    if cog is None:
        for filename in os.listdir('./cogs'):
            if filename.endswith('.py'):
                await ctx.message.add_reaction('<:loading:667529420013305857>')
                bot.load_extension(f'cogs.{filename[:-3]}')
                cog1 = 'all cogs'

    else:
        try:
            await ctx.message.add_reaction('<:loading:667529420013305857>')
            bot.load_extension(f"cogs.{cog}")
            cog1 = f'cog `{cog}`'
        except Exception as error:
            await ctx.message.clear_reactions()
            await ctx.send(f"{cog} can't be loaded")
            raise error

    await ctx.message.clear_reactions()
    await ctx.send(f'Successfully loaded {cog1}')


for cog in os.listdir(r"./cogs"):
    if cog.endswith(".py") and not cog.startswith("_"):
        try:
            cog = f"cogs.{cog.replace('.py', '')}"
            bot.load_extension(cog)
        except Exception as e:
            print(f"{cog} can not be loaded")
            raise e

bot.loop.run_until_complete(create_db_pool())
bot.run(os.environ['token'])
