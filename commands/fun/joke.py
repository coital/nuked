import discord, datetime, time, aiohttp
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(Joke(bot))

class Joke(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command()
    async def joke(self, ctx):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get("https://sv443.net/jokeapi/v2/joke/Any?type=single") as response:
                json = await response.json()
                embed = discord.Embed(title="**Joke**", color=util.get_color(),
                          description=f"{json['joke']}", timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                await ctx.send(util.embed_to_str(embed), delete_after=25)
                await session.close()
    