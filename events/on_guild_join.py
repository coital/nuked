import discord, datetime, asyncio
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(OnGuildJoin(bot))

class OnGuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_message_join(self, guild):
        util.log(f'A guild was joined: {guild.name}')
    