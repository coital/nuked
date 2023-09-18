import discord, datetime, time, aiohttp, wikipedia, bs4
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Wiki(bot))

class Wiki(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["wikipedia"])
    async def wiki(self, ctx, *, message):
        await ctx.message.delete()
        try:
            try:
                await ctx.send(wikipedia.summary(message, sentences=2))
            except UserWarning:
                pass
            except bs4.GuessedAtParserWarning:
                pass
        except Exception as e:
            await ctx.send(e)
    