import discord, datetime
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Query(bot))

class Query(commands.Cog):
    @commands.command(aliases=["searchq"])
    async def query(self, ctx, *, message):
        await ctx.message.delete()
        embed = discord.Embed(title="**Search Query**", 
            color=util.get_color(), 
            description=f"https://google.com/search?q={message}".replace(" ", "+"), 
            timestamp=datetime.datetime.utcfromtimestamp(util.time.time()))
        await ctx.send(embed=embed, delete_after=25)
