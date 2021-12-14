import discord, datetime, asyncio
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(OnRelationshipAdd(bot))

class OnRelationshipAdd(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_relationship_add(self, friendship):
        util.log(f"A friend was added: [bold]{friendship.user.display_name}#{friendship.user.discriminator}[/bold].")
    