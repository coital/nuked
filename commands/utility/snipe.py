import discord, datetime, asyncio
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Snipe(bot))

class Snipe(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def snipe(self, ctx):
        await ctx.message.delete()
        currentChannel = ctx.channel.id
        if currentChannel in self.client.sniped_message_dict:
            await ctx.send(f"{self.client.sniped_message_dict[currentChannel]}", delete_after=20)
        else:
            await ctx.send("there are no messages to snipe.", delete_after=5)
    