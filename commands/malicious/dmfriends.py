# is this how i'm supposed to do it? 

import asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(DMFriends(bot))

class DMFriends(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["dmf"])
    async def dmfriends(self, ctx, *, message: str = None):
        await ctx.message.delete()
        for user in self.client.user.friends:
            try:
                await user.send(f"{message}")
                await asyncio.sleep(0.5)
            except:
                util.log(f"DMFriends failed to DM {user}, sleeping for 0.5", error=True)
                await asyncio.sleep(0.5)
        
                
        
    