import discord, datetime, time
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(Splash(bot))

class Splash(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def splash(self, ctx):
        await ctx.message.delete()
        util.splash()