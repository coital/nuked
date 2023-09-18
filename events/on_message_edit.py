import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(OnMessageEdit(bot))

class OnMessageEdit(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener() 
    async def on_message_edit(self, before, after):
        await self.client.process_commands(after)
    