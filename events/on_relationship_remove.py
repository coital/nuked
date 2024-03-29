import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(OnRelationshipRemove(bot))

class OnRelationshipRemove(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_relationship_remove(self, friendship):
        util.log(f"A friend was removed: [bold]{friendship.user.name}[/bold].")
    