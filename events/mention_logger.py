import discord, json, time, aiohttp, json
from colorama import Fore, Style
from discord.ext import commands
from modules import util

with open("./config.json") as f:
    config = json.load(f)

mention_logger = config["Enable Mention Logger"]

def setup(bot: commands.Bot):
    bot.add_cog(MentionLogger(bot))

class MentionLogger(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener("on_message")
    async def _(self, message):
        if mention_logger:
            if message.author == self.client.user:
                return
            if self.client.user.mentioned_in(message):
                util.log(f"[bold]{message.author}[/bold] mentioned you in {message.guild.name if message.guild else 'DMs'}: [green][bold]{message.content.replace(f'<@{self.client.user.id}>', f'@{self.client.user.display_name}#{self.client.user.discriminator}').replace(f'<@!{self.client.user.id}>', f'@{self.client.user.display_name}#{self.client.user.discriminator}')}[/bold][/green]")