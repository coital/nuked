import discord, datetime, base64
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Base64(bot))

class Base64(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def base64(self, ctx, option: str = None, *, message: str = None):
        await ctx.message.delete()
        if not option:
            embed = discord.Embed(
                    title=f"**Base64**", color=util.get_color(), 
                    description=f"Encode or decode Base64 strings.", 
                    timestamp=datetime.datetime.utcfromtimestamp(util.time.time()))
            embed.add_field(name="**Encoding to Base64**", value=f"to encode a string into Base64, use `{self.client.command_prefix}base64 encode <string>`.", inline=False)
            embed.add_field(name="**Encoding from Base64**", value=f"to decode a string from Base64, use `{self.client.command_prefix}base64 decode <string>`.", inline=False)
            await ctx.send(embed=embed, delete_after=25)

        match option.lower():
            case "encode":
                if message:
                    await ctx.send(base64.b64encode(bytes(message, 'utf-8')).decode())
            case "decode":
                if message:
                    await ctx.send(base64.b64decode(bytes(message, 'utf-8')).decode())
