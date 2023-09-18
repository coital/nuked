import discord, datetime, asyncio
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(Bump(bot))

class Bump(commands.Cog):
    @commands.command()
    async def bump(self, ctx):
        await ctx.message.delete()
        await ctx.send("Starting..", delete_after=5)
        while True:
            try:
                await ctx.send("!d bump", delete_after=20)
                await asyncio.sleep(7200)
            except Exception as e:
                util.log(f"Couldn't bump in {ctx.channel.id}. Did the channel get nuked or deleted? Error: {e}", error=True)
    