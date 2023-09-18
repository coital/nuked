import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(OnGuildJoin(bot))

class OnGuildJoin(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_guild_join(self, guild):
        util.log(f"A guild was joined: [bold]{guild.name}[/bold]")
    