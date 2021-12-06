import discord, datetime, time
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Light(bot))

class Light(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def light(self, ctx, option: str=None):
        await ctx.message.delete()
        if not option:
            embed = discord.Embed(
                                title=f"**Light Mode**", color=0xFFFAFA, 
                                description=f"Light mode is an \"event-only\" mode, where Nuked will not respond to commands.\nIt significantly reduces the time it takes for events to respond.\nTo enable light mode, tweak config.json, or use `{self.client.command_prefix}light on`\n\nTo enable commands, you must restart Nuked.", 
                                timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=20)
        elif option.lower() == "on":
            embed = discord.Embed(title=f"**Enabling light mode**", color=0xFFFAFA,
                              description="Detaching all commands to reduce the time an event takes to respond.\nTo enable commands, you must restart Nuked.", timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=20)
            self.client.recursively_remove_all_commands()
            util.log(f"Light mode is enabled - commands will not work.")
    