import discord
from discord.ext import commands

class help(commands.Cog):
    
    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    async def help(self, ctx):
        """Shows this message"""
        #cmdlist = []
        cmdembed = discord.Embed(color=ctx.author.color, title=f'Available commands for {ctx.author.display_name}:', footer=f'Requested by {ctx.author}')
        for cmd in self.bot.commands:
            try:
                await cmd.can_run(ctx)
                #cmdlist.append(cmd.name)
                cmdembed.add_field(name=f'**{cmd.name} {cmd.signature}**', value=(cmd.help if cmd.help else "None"))
            except:
                pass
        #embedcmds = discord.Embed(color=ctx.author.color, title=f'Available commands for {ctx.author.display_name}:', description='\n'.join(cmdlist), footer=f'Requested by {ctx.author}')
        #await ctx.send('**Commands you can use:**\n' + '\n'.join(cmdlist))
        await ctx.send(embed=cmdembed)



def setup(bot):
    bot.add_cog(help(bot))
    