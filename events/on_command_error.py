import discord, json, re, time, aiohttp
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(CommandError(bot))

class CommandError(commands.Cog):
    @commands.Cog.listener()
    async def on_command_error(self, ctx, error):
        error_str = str(error)
        _error = getattr(error, 'original', error)
        if isinstance(_error, commands.CommandNotFound):
            return
        util.error(f'{ctx.command} - {error_str}')