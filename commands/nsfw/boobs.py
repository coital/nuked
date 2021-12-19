import aiohttp, discord, hmtai, requests
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Boobs(bot))
class Boobs(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def boobs(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/boobs")
        embed = discord.Embed(
            color=util.get_color(), timestamp=util.datetime.datetime.utcfromtimestamp(util.time.time()))
        embed.set_image(url=r.json()['url'])
        await ctx.send(embed=embed, delete_after=20)
                