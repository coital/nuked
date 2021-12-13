import discord, json, time, aiohttp, json
from colorama import Fore, Style
from discord.ext import commands
from modules import util

with open("./config.json") as f:
    config = json.load(f)

mentionblocker = config["Enable Mention Blocker"]

def setup(bot: commands.Bot):
    bot.add_cog(MentionBlocker(bot))

class MentionBlocker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener("on_message")
    async def _(self, message):
        if mentionblocker:
            if self.client.user.mention in message.content:
                guild = message.guild
                try:
                    await guild.ack()
                except:
                    pass