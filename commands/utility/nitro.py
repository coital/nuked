import discord, datetime, time, random, aiohttp, json
from discord.ext import commands
from modules import util

async def setup(bot: commands.Bot):
    await bot.add_cog(Nitro(bot))

with open("./config.json") as f:
    config = json.load(f)

token = config["Discord Token"]

class Nitro(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def nitro(self, ctx, option: str=None, code: str = None):
        await ctx.message.delete()
        embed = discord.Embed(
                            title=f"**Nitro Tools**", color=util.get_color(), 
                            description=f"Tools to check or generate Nitro codes.", 
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**Check a Nitro Code**", value=f"to check a Nitro code, use `{self.client.command_prefix}nitro check <code>`.", inline=False)
        embed.add_field(name="**Generate a Nitro Code**", value=f"to generate a Nitro code, use `{self.client.command_prefix}nitro generate`.", inline=False)
        if not option:
            await ctx.send(util.embed_to_str(embed), delete_after=20)
        elif option.lower() == "generate" or option.lower() == "gen":
            await ctx.send("https://discord.gift/" + "".join(random.choices("ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijlkmnopqrstuvwxyz1234567890", k=16)))
        elif option.lower() == "check":
            if not code:
                await ctx.send(util.embed_to_str(embed), delete_after=20)
            stripped_code = code.removeprefix("https://discord.gift/")
            async with aiohttp.ClientSession(headers={"authorization": token, "user-agent": "Mozilla/5.0"}) as session:
                async with session.post(url=f"{util.utd_api}/entitlements/gift-codes/{stripped_code}/redeem", json={"channel_id": ctx.channel.id}) as response:
                    if response.ok:
                        await ctx.send(f"code {stripped_code} is valid")
                    else:
                        await ctx.send(f"code {stripped_code} is not valid")
        
                        