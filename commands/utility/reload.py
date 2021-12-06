import os, datetime, time, discord, sys
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
        bot.add_cog(Reload(bot))

class Reload(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["rl"])
    async def reload(self, ctx, arg: str = None):
        await ctx.message.delete()
        if not arg:
            embed = discord.Embed(title="**Reload**", description=f"Reload Nuked or reload all commands for Nuked.",
                              color=0xFAFAFA, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name="**Reloading Nuked**", value=f"to reload Nuked, use `{self.client.command_prefix}reload nuked`, `{self.client.command_prefix}reload sb` or `{self.client.command_prefix}reload selfbot`.", inline=False)
            embed.add_field(name="**Reloading Cogs**", value=f"to reload cogs, use `{self.client.command_prefix}reload cogs` or `{self.client.command_prefix}reload commands`.", inline=False)
            await ctx.send(embed=embed, delete_after=20)
        elif arg.lower() == "cogs" or arg.lower() == "commands":
            for command in util.load_commands():
                self.client.unload_extension(command)
                self.client.load_extension(command)
            await ctx.send(f"reloaded {len(util.load_commands())} cogs.", delete_after=15)
        elif arg.lower() == "nuked" or arg.lower() == "sb" or arg.lower() == "selfbot":
            util.clear()
            os.system('python "' + os.getcwd() + "\\" + sys.argv[0] + '"')
                
        
    