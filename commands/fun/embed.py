import discord, datetime, time
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Embed(bot))

class Embed(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["say"])
    async def embed(self, ctx, *, message: str):
        await ctx.message.delete()
        embed = discord.Embed(color=util.get_color(), description=message,
                          timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.set_author(name=str(self.client.user.display_name + "#" +
                              self.client.user.discriminator), icon_url=self.client.user.avatar_url)
        await ctx.send(util.embed_to_str(embed), delete_after=20)
    