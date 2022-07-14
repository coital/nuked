import discord, datetime, time, requests
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
        embed = discord.Embed(title="**Nuked | Help**",
                              color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**Fun Commands**",
                        value=f"{self.client.command_prefix}help fun", inline=False)
        embed.add_field(name="**NSFW Commands**",
                        value=f"{self.client.command_prefix}help nsfw", inline=False)
        embed.add_field(name="**Malicious Commands**",
                        value=f"{self.client.command_prefix}help malicious", inline=False)
        embed.add_field(name="**Utility Commands**",
                        value=f"{self.client.command_prefix}help util", inline=False)
        if not option:
            try:
                await ctx.send(util.embed_to_str(embed), delete_after=25)
            except discord.HTTPException:
                print(util.embed_to_str(embed))
                await ctx.send(util.embed_to_str(embed), delete_after=25)
        elif option.lower() == "fun":
            embed = discord.Embed(title="**Fun Commands**", description="<> - required\n[] - optional",
            color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name=f"**{self.client.command_prefix}ascii <text>**", value="Send <text> in ASCII art.")
            embed.add_field(name=f"**{self.client.command_prefix}cat**", value="Send a random image of a cat.")
            embed.add_field(name=f"**{self.client.command_prefix}clyde <message>**", value="Send an image of Discord's Clyde saying <message>.")
            embed.add_field(name=f"**{self.client.command_prefix}hug [mentioned user]**", value="Send a random hugging gif.")
            embed.add_field(name=f"**{self.client.command_prefix}joke**", value="Send a random joke.")
            embed.add_field(name=f"**{self.client.command_prefix}kiss [mentioned user]**", value="Send a random kissing gif.")
            embed.add_field(name=f"**{self.client.command_prefix}linespam <amount> <message>**", value="Spam multiple lines of <message> <amount> time(s).")
            embed.add_field(name=f"**{self.client.command_prefix}phcomment <username> <message>**", value="Send a fake image of a PornHub comment with <message> from <user>.")
            embed.add_field(name=f"**{self.client.command_prefix}spam <amount> <message>**", value="Spam <message> <amount> time(s).")
            embed.add_field(name=f"**{self.client.command_prefix}trumptweet <message>**", value="Send a fake image of Donald Trump tweeting <message>.")
            embed.add_field(name=f"**{self.client.command_prefix}tweet <username> <message>**", value="Send a fake image of <username> tweeting <message>.")
            embed.add_field(name=f"**{self.client.command_prefix}ud <query>**", value="Query Urban Dictionary for <query>, and send the most relevant result.")
            embed.add_field(name=f"**{self.client.command_prefix}wiki <query>**", value="Query Wikipedia for <query>, and send the most relevant result.")
            embed.add_field(name=f"**{self.client.command_prefix}wyr**", value="Send a random Would You Rather question.")
            await ctx.send(util.embed_to_str(embed), delete_after=25)
        elif option.lower() == "nsfw":
            embed = discord.Embed(title="**NSFW Commands**", description="<> - required\n[] - optional",
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name=f"**{self.client.command_prefix}boobs**", value="Send a random embedded image of anime boobs.")
            embed.add_field(name=f"**{self.client.command_prefix}hentai <category>**", value="Send an embedded hentai gif or image, based on <category>. Use the command to view the categories.")
            await ctx.send(embed=embed, delete_after=25)
        elif option.lower() == "malicious":
            embed = discord.Embed(title="**Malicious Commands**", description="<> - required\n[] - optional",
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name=f"**{self.client.command_prefix}crash**", value="Spam a multitude of emojis and characters in attempt to crash or lag a user's Discord client.")
            embed.add_field(name=f"**{self.client.command_prefix}massdm <message>**", value="DM everybody in the server <message>.")
            await ctx.send(util.embed_to_str(embed), delete_after=25)
        elif option.lower() == "util" or option.lower() == "utility":
            embed = discord.Embed(title="**Utility Commands | Page 1**", description="<> - required\n[] - optional",
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name=f"**{self.client.command_prefix}avatar [mentioned user]**", value="Send an embedded image or gif of the user's avatar.")
            embed.add_field(name=f"**{self.client.command_prefix}base64 <option> <message>**", value="Encode or decode <message> to or from Base64.")
            embed.add_field(name=f"**{self.client.command_prefix}backup <option>**", value="Create a backup of friends, servers, or both.")
            embed.add_field(name=f"**{self.client.command_prefix}bump**", value="Send d!bump in the channel every 2 hours")
            embed.add_field(name=f"**{self.client.command_prefix}cacheall [limit]**", value="Create a text file containing every message and attachment where the command is ran at. The default limit is 10000, but can be altered by [limit].")
            embed.add_field(name=f"**{self.client.command_prefix}dmpurge [limit]**", value="Delete [limit] messages in a DM or Group. The default limit is 10000, but can be altered by [limit].")
            embed.add_field(name=f"**{self.client.command_prefix}eval <command>**", value="Execute <command>, and send the output.")
            embed.add_field(name=f"**{self.client.command_prefix}latency**", value="Send client latency.")
            embed.add_field(name=f"**{self.client.command_prefix}light <option>**", value="Enable or disable Light Mode.")
            embed.add_field(name=f"**{self.client.command_prefix}nitro <option> [code]**", value="Generate or check a Discord Nitro code.")
            embed.set_footer(text=f"To view more utility commands, use {self.client.command_prefix}help {option.lower()} 2")

            await ctx.send(util.embed_to_str(embed), delete_after=25)
        elif option.lower() == "util 2" or option.lower() == "utility 2":
            embed = discord.Embed(title="**Utility Commands | Page 2**", description="<> - required\n[] - optional",
                                   color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
            embed.add_field(name=f"**{self.client.command_prefix}prefix [prefix]**", value="View or change the current prefix.")
            embed.add_field(name=f"**{self.client.command_prefix}purge <amount>**", value="Delete <amount> messages sent by you.")
            embed.add_field(name=f"**{self.client.command_prefix}reload <option>**", value="Reload commands or Nuked.")
            embed.add_field(name=f"**{self.client.command_prefix}settings**", value="Send an embed of your current settings for Nuked.")
            embed.add_field(name=f"**{self.client.command_prefix}snipe**", value="Send a previously deleted message.")
            embed.add_field(name=f"**{self.client.command_prefix}splash**", value="Reset the console's screen back to the splash.")
            embed.add_field(name=f"**{self.client.command_prefix}status <type> <message>**", value="Change your user status to <type> and <message>.")
            embed.add_field(name=f"**{self.client.command_prefix}theme [theme]**", value="View or change Nuked's current theme.")
            embed.add_field(name=f"**{self.client.command_prefix}token <option> [token]**", value="Generate or check a token.")
            embed.add_field(name=f"**{self.client.command_prefix}webhook <option> [webhook] [content]**", value="View information for, send content to, or delete a Discord webhook.")
            embed.add_field(name=f"**{self.client.command_prefix}logout**", value="Log out of Nuked and exit the process.")
            await ctx.send(util.embed_to_str(embed), delete_after=25)
