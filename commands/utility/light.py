import discord, datetime, time
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(Light(bot))

class Light(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def light(self, ctx, option: str=None):
        await ctx.message.delete()
        if not option:
            embed = discord.Embed(title=f"**Light Mode**", color=util.get_color(),  description=f"Light mode is an \"event-only\" mode, where Nuked will not respond to commands.\nIt significantly reduces the time it takes for events to respond.\nTo enable light mode, tweak config.json, or use `{self.client.command_prefix}light on`\n\nTo enable commands, you must restart Nuked.", 
                                timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(util.embed_to_str(embed), delete_after=20)
        elif option.lower() == "on":
            new_json = util.get_config()
            new_json["Enable Light Mode"] = True
            with open("./config.json", "w+") as f:
                util.json.dump(new_json, f, indent=4)
            embed = discord.Embed(title=f"**Enabling light mode**", color=util.get_color(),
                              description=f"Detaching all commands to reduce the time an event takes to respond.\nTo enable commands, you must use `{self.client.command_prefix}light off`.", timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            # await ctx.send(embed=embed, delete_after=20)
            for command in util.enable_light_mode():
                await self.client.unload_extension(command)
            util.log(f"Light mode is enabled - commands will not work.")
        elif option.lower() == "off":
            if not util.get_config()["Enable Light Mode"]:
                await ctx.send("light mode is not enabled.", delete_after=10)
                return
            new_json = util.get_config()
            new_json["Enable Light Mode"] = False
            with open("./config.json", "w+") as f:
                util.json.dump(new_json, f, indent=4)
            for command in util.enable_light_mode():
                await self.client.load_extension(command)
            embed = discord.Embed(title=f"**Disabling light mode**", color=util.get_color(),
                              description="Reattaching all commands. This may increase the time events take to respond.", timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            util.log(f"Light mode was disabled - commands will now work.")
            await ctx.send(util.embed_to_str(embed), delete_after=20)
    