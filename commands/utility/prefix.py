import discord, datetime, time
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Prefix(bot))

class Prefix(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["setprefix"])
    async def prefix(self, ctx, *, new_prefix: str = None):
        await ctx.message.delete()
        if not new_prefix:
            embed = discord.Embed(title="**Nuked | Prefix**", description=f"The current prefix is `{self.client.command_prefix}`,\nbut you can change it by using `{self.client.command_prefix}prefix <prefix>`",
                                  color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(util.embed_to_str(embed), delete_after=15)
        else:
            old_prefix = self.client.command_prefix
            self.client.command_prefix = new_prefix
            await ctx.send(f"changed prefix from `{old_prefix}` to `{new_prefix}`.", delete_after=10)
    