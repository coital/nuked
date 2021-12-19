import discord, datetime, time, requests
from bs4 import BeautifulSoup as bs4
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
        bot.add_cog(WYR(bot))

class WYR(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["wouldyourather"])
    async def wyr(self, ctx):
        await ctx.message.delete()
        r = requests.get("https://www.conversationstarters.com/wyrqlist.php").text
        soup = bs4(r, "html.parser")
        qa = soup.find(id="qa").text
        qor = soup.find(id="qor").text
        qb = soup.find(id="qb").text
        embed = discord.Embed(
            title="**Would You Rather?**",
            color=util.get_color(), 
            description=f"**{qa}**\n\n{qor}\n\n**{qb}**", 
            timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        await ctx.send(embed=embed, delete_after=25)
    