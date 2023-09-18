import discord, datetime, base64, signal
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(Logout(bot))

class Logout(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["exit"])
    async def logout(self, ctx):
        await ctx.message.delete()
        signal.raise_signal(signal.SIGINT)
