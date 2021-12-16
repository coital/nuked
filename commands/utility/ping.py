import discord, os, re
from modules import util
from discord.ext import commands
import pythonping

def setup(bot: commands.Bot):
    bot.add_cog(Ping(bot))

class Ping(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["testping"])
    async def testping(self, ctx, ip: str="1.1.1.1"):
        await ctx.message.delete()
        await ctx.send(pythonping.ping(ip), delete_after=20)
        
    