import discord
from discord.ext import commands

def check_guild(guild):
    async def predicate(ctx):
        if ctx.guild.id == guild:
            return True
        else:
            return False
    return commands.check(predicate)

class spv2(commands.Cog):

    def __init__(self, bot):
        self.bot = bot

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def danny(self, ctx):
        """Shows how cool Danny is"""
        await ctx.send('Danny is super epic')

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def jack(self, ctx):
        """Exposes Jack's location"""
        await ctx.send('jack lives in slough')

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def spez(self, ctx):
        """He sucks a lot"""
        await ctx.send('spezsucksalot sucks a lot')
    
    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def mel(self, ctx):
        """The best"""
        await ctx.send('Arctic Monkeys is the best band ever and anyone who disagrees is automatically my enemy')

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def niz(self, ctx):
        """Super epic"""
        await ctx.send('Niz has an epic vibe')

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def locke(self, ctx):
        """Minecraft"""
        await ctx.send('He do be advertising his minecraft server doe ||it\'s called E-Shack you should check it out||')

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def rarity(self, ctx):
        """Loves chipotle"""
        await ctx.send("World's biggest Chipotle fan")

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def doot(self, ctx):
        """Annoy fromch"""
        await ctx.send("<@420788676516249601> get pinged lol")

    @commands.command(aliases=['gamer','fake','fg'])
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def fakegamer(self, ctx):
        """Don't lie to yourselves"""
        fakeEmbed = discord.Embed()
        fakeEmbed.set_image(url='https://cdn.discordapp.com/attachments/665249180150792216/696875431697055773/image0.jpg')
        await ctx.send(embed=fakeEmbed)
    
    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    #@commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def matthew(self, ctx):
        await ctx.send("Daddy Matthew ❤️")

    @commands.command()
    @commands.has_any_role(699009243143209071, 665323670868197376, 665296778844700712, 681162165725560886, 699260354231795773, 681163948149702776)
    async def awooga(self, ctx):
        await ctx.send("sees woman \n \n My jaw drops to the floor, my eyes extend at a velocity never before seen, I take out a boxing glove and hit myself with it 17 times, pant like a dog, and yell AOOOOGA AOOOOGA then turn to the audience and say in 1930’s New York accent “HOT MAMA, now that’s a dame!”")

def setup(bot):
    bot.add_cog(spv2(bot))