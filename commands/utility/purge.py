import discord, datetime, time
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Purge(bot))

class Purge(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["clear"])
    async def purge(self, ctx, amount: int = 1):
        await ctx.message.delete()
        async for message in ctx.channel.history(limit=amount):
            if message.author == self.client.user:
                await message.delete()
    