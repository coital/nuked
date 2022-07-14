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
        r = requests.get("https://nekobot.xyz/api/image?type=boobs")
        embed = discord.Embed(
            color=util.get_color(), timestamp=util.datetime.datetime.utcfromtimestamp(util.time.time()))
        embed.set_image(url=r.json()['message'])
        await ctx.send(util.embed_to_str(embed), delete_after=20)
                