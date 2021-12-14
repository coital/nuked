import discord, os, re
from modules import util
from discord.ext import commands

def setup(bot: commands.Bot):
    bot.add_cog(DmPurge(bot))

class DmPurge(commands.Cog):
    def __init__(self, bot):
        self.client = bot
    @commands.command(aliases=["purgeall"])
    async def dmpurge(self, ctx, limit: int = 20000):
        await ctx.message.delete()
        if isinstance(ctx.channel, discord.channel.DMChannel) or isinstance(ctx.channel, discord.channel.GroupChannel):
            async for message in ctx.history(limit=limit):
                if message.author == self.client.user:
                    try:
                        await message.delete()
                    except Exception as e:
                        util.error(f"Could not delete message: [bold]{str(e)}[/bold]")
        else:
            await ctx.send("channel is not a group or DM.", delete_after=10)
        
    