import discord, os, re
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(CacheAll(bot))

bad_chars = r"[\\/\*\|<>:\"]"

class CacheAll(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["cache", "history", "getall"])
    async def cacheall(self, ctx, limit: int = 10000):
        await ctx.message.delete()
        if not os.path.isdir("Cached Messages"):
            os.mkdir("Cached Messages")
        with open(f"./Cached Messages/{re.sub(bad_chars, '', ctx.guild.name)}.{re.sub(bad_chars, '', ctx.channel.name)}.txt" if ctx.guild else f"./Cached Messages/{re.sub(bad_chars, '', ctx.channel.name)}.messages.txt", "a") as f:
            async for message in ctx.history(limit=limit):
                try:
                    if message.attachments:
                        util.log(f"Cached attachment URL: {message.attachments[0].url}")
                        f.write(f"\n{message.created_at} - User \"{message.author}\": {message.attachments[0].url}\n")
                    else:
                        util.log(f"Cached content: {message.content}")
                        f.write(f"\n{message.created_at} - User \"{message.author}\": {message.content}\n")
                except Exception as e:
                    util.log(f"Exception thrown while caching, message: {e}", error=True)
                    continue
        
    