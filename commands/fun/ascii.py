import discord, datetime, time, aiohttp, pyfiglet
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(Ascii(bot))

class Ascii(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def ascii(self, ctx, *, message):
        await ctx.message.delete()
        result = pyfiglet.figlet_format(message)
        if len(result) > 1992:
            return
        else:
            await ctx.send('```' + result + '```')
    