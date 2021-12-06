import discord, datetime, time
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(Linespam(bot))

class Linespam(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["ls"])
    async def linespam(self, ctx, amount: int, *, message):
        await ctx.message.delete()
        for _ in range(amount):
            await ctx.send(f'{message}\n' * 15)
    