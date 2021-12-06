import discord, json, time, aiohttp, json
from colorama import Fore, Style
from discord.ext import commands
from modules import util
from win10toast import ToastNotifier
toaster = ToastNotifier()

with open("./config.json") as f:
    config = json.load(f)

mentionblocker = config.get("block_mentions")

def setup(bot: commands.Bot):
    bot.add_cog(MentionBlocker(bot))

class MentionBlocker(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener()
    async def on_message(self, message):
        if mentionblocker:
            if self.client.user.mention in message.content:
                guild = message.guild
                try:
                    await guild.ack()
                except:
                    pass