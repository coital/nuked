# is this how i'm supposed to do it? 

import asyncio
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(MassDM(bot))

class MassDM(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["mdm", "dmall"])
    async def massdm(self, ctx, *, message: str = None):
        await ctx.message.delete()
        for user in ctx.guild.members:
            if user != self.client.user:
                try:
                    await user.send(f"{message}")
                    await asyncio.sleep(0.5)
                except:
                    util.log(f"MassDM failed to DM {user}, sleeping for 0.5", error=True)
                    await asyncio.sleep(0.5)
        
                
        
    