import discord, datetime, time
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Spam(bot))

class Spam(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def spam(self, ctx, amount: int, *, message: str):
        await ctx.message.delete()
        for _ in range(amount):
            await ctx.send(f'{message}')
    