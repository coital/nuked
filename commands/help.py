import discord, datetime, time
from discord.ext import commands
from modules import util

# copied just a little bit from v5, shhh

def setup(bot: commands.Bot):
    bot.add_cog(Help(bot))

class Help(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def help(self, ctx, *, option: str = None):
        await ctx.message.delete()
        embed = discord.Embed(title="**Nuked | Help**", description=f"{util.version} - {self.client.user.name}#{self.client.user.discriminator}",
                              color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**Fun Commands**",
                        value=f"{self.client.command_prefix}help fun", inline=False)
        embed.add_field(name="**NSFW Commands**",
                        value=f"{self.client.command_prefix}help nsfw", inline=False)
        embed.add_field(name="**Malicious Commands**",
                        value=f"{self.client.command_prefix}help malicious", inline=False)
        embed.add_field(name="**Utility Commands**",
                        value=f"{self.client.command_prefix}help util\n{self.client.command_prefix}help util 2", inline=False)
        embed.set_thumbnail(url=self.client.user.avatar_url)
        embed.set_footer(
            text="Nuked", icon_url="https://cdn.discordapp.com/attachments/820836670857412710/820946025799745576/avatar.png")
        if not option:
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "fun":
            embed = discord.Embed(title="**Fun Commands**", description="not implemented mane", 
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "nsfw":
            embed = discord.Embed(title="**NSFW Commands**", description="not implemented mane", 
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "malicious":
            embed = discord.Embed(title="**Malicious Commands**", description="not implemented mane", 
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "util" or option.lower() == "utility":
            embed = discord.Embed(title="**Utility Commands | Page 1**", description="not implemented mane", 
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "util 2" or option.lower() == "utility 2":
            embed = discord.Embed(title="**Utility Commands | Page 2**", description="not implemented mane", 
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            await ctx.send(embed=embed, delete_after=25)