import discord, datetime, time, requests
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Kiss(bot))

class Kiss(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def kiss(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        r = requests.get("https://nekos.life/api/kiss")
        embed = discord.Embed(description=f"<@{self.client.user.id}> kisses {f'<@{member.id}>' if member else ''}",
                          color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.set_image(url=r.json()['url'])
        await ctx.send(util.embed_to_str(embed), delete_after=20)
    