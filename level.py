import discord
from discord.ext import commands
from datetime import date

class level(commands.Cog):

    def __init__(self, bot):
        self.bot = bot
        
    async def lvl_up(self, user):
        cur_xp = user['xp']
        cur_lvl = user['lvl']

        if cur_xp >= round((2 * (cur_lvl ** 5)) / 9):
            await self.bot.pg_con.execute("UPDATE users SET lvl = $1 WHERE user_id  = $2 AND guild_id = $3",
                                          cur_lvl + 1, user['user_id'], user['guild_id'])
            return True
        else:
            return False

    @commands.Cog.listener()
    async def on_message(self, message):
        if message.author == self.bot.user:
            return

        if message.author.bot:
            return

        #if message.guild.id != '665249179496349716':
            #return

        author_id = str(message.author.id)
        guild_id = str(message.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                           guild_id)
        
        today = date.today()
        dt = today.strftime("%b-%d-%Y")
        if not user:
            await self.bot.pg_con.execute(
                "INSERT INTO users (user_id, guild_id, lvl, xp, date) VALUES ($1, $2, 1, 0, $3)",
                author_id, guild_id, dt)


        user = await self.bot.pg_con.fetchrow("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                              guild_id)
        await self.bot.pg_con.execute("UPDATE users SET xp = $1 WHERE user_id = $2 AND guild_id = $3", user['xp'] + 1, author_id, guild_id)

        id = str(message.guild.id)
        if await self.lvl_up(user):
            if "695145238376874004" in id:
                pass
            if "665249179496349716" in id:
                channel = self.bot.get_channel(681185110120202367)
                embed = discord.Embed(color=message.author.color, title=f"{message.author} is now level {user['lvl'] + 1}")
                embed.set_author(name="Level up!", icon_url=message.author.avatar_url,)
                await channel.send(embed=embed)
            else:
                channel = message.channel
                embed = discord.Embed(color=message.author.color, title=f"{message.author} is now level {user['lvl'] + 1}")
                embed.set_author(name="Level up!", icon_url=message.author.avatar_url,)
                await channel.send(embed=embed)

    @commands.command(aliases=['lvl'])
    async def level(self, ctx, member: discord.Member = None):
        """Show's the user's level in the server"""
        member = ctx.author if not member else member
        author_id = str(member.id)
        guild_id = str(ctx.guild.id)

        user = await self.bot.pg_con.fetch("SELECT * FROM users WHERE user_id = $1 AND guild_id = $2", author_id,
                                           guild_id)

        if not user:
            await ctx.send("Member doesn't have a level yet!")
        else:
            embed = discord.Embed(color=member.color)

            embed.set_author(
                    name=f'Level - {member}', icon_url=member.avatar_url)

            embed.add_field(name='Level', value=user[0]['lvl'])
            embed.add_field(name='XP', value=user[0]['xp'])
            embed.set_footer(text=f"XP needed to level up: {round((2 * (user[0]['lvl'] ** 5)) / 9)}")

            await ctx.send(embed=embed)


        
            
def setup(bot):
    bot.add_cog(level(bot))