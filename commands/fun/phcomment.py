import discord, datetime, time, aiohttp
from modules import util
from discord.ext import commands

async def setup(bot: commands.Bot):
    await bot.add_cog(PHComment(bot))

class PHComment(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["pornhub"])
    async def phcomment(self, ctx, username, *, message):
        await ctx.message.delete()
        async with aiohttp.ClientSession() as session:
            async with session.get(f"https://nekobot.xyz/api/imagegen?type=phcomment&text={message}&username={username}&image=https://i.imgur.com/raRKTgZ.jpg") as response:
                r = await response.json()
                embed = discord.Embed(
                    color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                embed.set_image(url=r["message"])
                
                await ctx.send(util.embed_to_str(embed), delete_after=20)
    