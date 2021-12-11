import aiohttp, discord, hmtai
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Hentai(bot))
class Hentai(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def hentai(self, ctx):
        await ctx.message.delete()
        categories = ["ahegao", "ass", "bdsm", "blowjob", "cuckold", "cum", "ero", "femdom", "foot", "gangband", "hentai", "hnt_gifs", "jahy", "manga", "mW", "nsfwMW", "nsfwNeko", "orgy", "panties", "pussy", "sfwNeko", "uniform", "wallpaper"]
        embed = discord.Embed(
            color=util.get_color(), timestamp=util.datetime.datetime.utcfromtimestamp(util.time.time()))
        embed.set_image(url=hmtai.useHM("1", util.random.choice(categories)))
        await ctx.send(embed=embed, delete_after=20)
                