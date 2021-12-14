import discord, datetime, time
from modules import util
from discord.ext import commands
from urbandictionary_top import udtop

def setup(bot: commands.Bot):
    bot.add_cog(UrbanDictionary(bot))

class UrbanDictionary(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["urban", "urbandictionary"])
    async def ud(self, ctx, *, message: str):
        await ctx.message.delete()
        await ctx.send(udtop(message))
    