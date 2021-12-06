import discord
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Latency(bot))

class Latency(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["ping"])
    async def latency(self, ctx):
        await ctx.message.delete()
        await ctx.send(f"Client latency is {int(round(self.client.latency * 1000))} ms", delete_after=20)
    