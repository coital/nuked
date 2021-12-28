import discord, datetime, time, requests
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(Cat(bot))

class Cat(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def cat(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/v2/img/meow")
        embed = discord.Embed(
            color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.set_image(url=r.json()['url'])
        await ctx.send(embed=embed, delete_after=20)
    