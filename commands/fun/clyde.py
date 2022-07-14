import discord, datetime, time, aiohttp
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(Clyde(bot))

class Clyde(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["discord"])
    async def clyde(self, ctx, *, message):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekobot.xyz/api/imagegen?type=clyde&text={message}") as response:
                r = await response.json()
                embed = discord.Embed(
                    color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_image(url=r["message"])
                await ctx.send(util.embed_to_str(embed), delete_after=20)
    