import os, datetime, time, discord
from discord.ext import commands
from modules import util
from discord import ActivityType

async def setup(bot: commands.Bot):
    await bot.add_cog(Status(bot))

class Status(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command(aliases=["activity"])
    async def status(self, ctx, type: str = None, *, message: str = "Nuked"):
        await ctx.message.delete()
        if not type:
            embed = discord.Embed(
                            title="Status Types", 
                            color=util.get_color(), 
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name="**playing**", value=f"have a `playing` status.\nUsage: `{self.client.command_prefix}status playing <text>`", inline=False)
            embed.add_field(name="**competing**", value=f"have a `competing` status.\nUsage: `{self.client.command_prefix}status competing <text>`", inline=False)
            embed.add_field(name="**listening**", value=f"have a `listening` status.\nUsage: `{self.client.command_prefix}status listening <text>`", inline=False)
            embed.add_field(name="**watching**", value=f"have a `watching` status.\nUsage: `{self.client.command_prefix}status watching <text>`", inline=False)
            embed.add_field(name="**streaming**", value=f"have a `streaming` status.\nUsage: `{self.client.command_prefix}status streaming <text>`", inline=False)
            await ctx.send(util.embed_to_str(embed), delete_after=20)
        elif type.lower() == "playing":
            await self.client.change_presence(activity=discord.Game(name=message), status=discord.Status.dnd)
            await ctx.send(f"set status to `playing {message}`", delete_after=10)
        elif type.lower() == "competing":
            await self.client.change_presence(activity=discord.Activity(name=message, type=ActivityType.competing), status=discord.Status.dnd)
            await ctx.send(f"set status to `competing {message}`", delete_after=10)
        elif type.lower() == "listening":
            await self.client.change_presence(activity=discord.Activity(type=discord.ActivityType.listening, name=message), status=discord.Status.dnd)
            await ctx.send(f"set status to `listening to {message}`", delete_after=10)
        elif type.lower() == "watching":
            await self.client.change_presence(activity=discord.Activity(type=ActivityType.watching, name=message), status=discord.Status.dnd)
            await ctx.send(f"set status to `watching {message}`", delete_after=10)
        elif type.lower() == "streaming":
            await self.client.change_presence(activity=discord.Activity(type=ActivityType.streaming, name=message), status=discord.Status.dnd)
            await ctx.send(f"set status to `streaming {message}`", delete_after=10)
        else:
            await ctx.send(f"invalid type, use {self.client.command_prefix}status to see all possible types.", delete_after=10)