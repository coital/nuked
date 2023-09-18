import discord
from discord.ext import commands
from modules import util


disable_eval = util.get_config()["Disable Eval Command"]

async def setup(bot: commands.Bot):
    await bot.add_cog(Eval(bot))

class Eval(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(name="eval")
    async def _(self, ctx, *, cmd=None):
        await ctx.message.delete()
        if disable_eval:
                util.log("The eval command is very dangerous! Be careful how you use it.")
                util.log("If you want to enable it, set the \"Disable Eval Command\" value from true to false in config.json.")
                return
        else:
            if not cmd:
                await ctx.send("eval is missing an argument.", delete_after=10)
            else:  
                cmd = cmd.strip("` ")
                cmd = "\n".join(f"    {i}" for i in cmd.splitlines())
                fn_name = "_eval_expr"
                body = f"async def {fn_name}():\n{cmd}"
                parsed = util.ast.parse(body)
                body = parsed.body[0].body
                util.insert_returns(body)
                env = {
                    "self": self,
                    "client": self.client,
                    "discord": discord,
                    "commands": commands,
                    "ctx": ctx,
                    "__import__": __import__,
                    "token": util.get_config()["Discord Token"],
                    "requests": util.requests,
                    "print": print,
                    "os": util.os,
                    "sys": util.sys,
                    "asyncio": util.asyncio,
                    "time": util.time,
                    "datetime": util.datetime,
                    "util": util
                }
                exec(compile(parsed, filename="<ast>", mode="exec"), env)

                result = (await eval(f"{fn_name}()", env))
                try:
                    await ctx.send(result)
                except:
                    pass
    