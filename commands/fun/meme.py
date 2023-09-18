import discord, datetime, time, requests
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Meme(bot))

class Meme(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def meme(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://some-random-api.ml/meme")
        embed = discord.Embed(
            color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.set_image(url=r.json()['image'])
        await ctx.send(util.embed_to_str(embed), delete_after=20)
    