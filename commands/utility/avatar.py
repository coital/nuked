import discord, datetime
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Avatar(bot))

class Avatar(commands.Cog):
    @commands.command(aliases=["av"])
    async def avatar(self, ctx, member: discord.Member = None):
        await ctx.message.delete()
        if not member:
            member = ctx.author
        embed = discord.Embed(title=f"{member}'s avatar", color=util.get_color(),
                            timestamp=datetime.datetime.utcfromtimestamp(util.time.time()))
        embed.set_image(url=member.avatar_url)
        await ctx.send(util.embed_to_str(embed), delete_after=25)
    