import discord, datetime, time
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(Theme(bot))

class Theme(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["settheme"])
    async def theme(self, ctx, *, new_theme: str = None):
        await ctx.message.delete()
        if not new_theme:
            embed = discord.Embed(title="**Nuked | Theme**", description=f"The current theme is `{util.get_config()['Theme']}`,\nbut you can change it by using `{self.client.command_prefix}theme <theme>`",
                                  color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=15)
        else:
            match new_theme.lower():
                case "light pink":
                    new_json = util.get_config()
                    old_theme = util.get_config()["Theme"]
                    new_json["Theme"] = new_theme
                    with open("./config.json", "w+") as f:
                        util.json.dump(new_json, f, indent=4)
                    await ctx.send(f"changed theme from `{old_theme}` to `{new_theme}`.", delete_after=10)
                case "light blue":
                    new_json = util.get_config()
                    old_theme = util.get_config()["Theme"]
                    new_json["Theme"] = new_theme
                    with open("./config.json", "w+") as f:
                        util.json.dump(new_json, f, indent=4)
                    await ctx.send(f"changed theme from `{old_theme}` to `{new_theme}`.", delete_after=10)
                case "default":
                    new_json = util.get_config()
                    old_theme = util.get_config()["Theme"]
                    new_json["Theme"] = new_theme
                    with open("./config.json", "w+") as f:
                        util.json.dump(new_json, f, indent=4)
                    await ctx.send(f"changed theme from `{old_theme}` to `{new_theme}`.", delete_after=10)
                case "reset":
                    new_json = util.get_config()
                    old_theme = util.get_config()["Theme"]
                    new_json["Theme"] = "Default"
                    with open("./config.json", "w+") as f:
                        util.json.dump(new_json, f, indent=4)
                    await ctx.send(f"reset the theme.", delete_after=10)
    