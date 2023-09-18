import discord, json, re, time, aiohttp, math
from discord.ext import commands
from modules import util

with open("./config.json") as f:
    config = json.load(f)

async def setup(bot: commands.Bot):
    await bot.add_cog(SlotbotSniper(bot))

slotbot = config["Enable Slotbot Sniper"]

class SlotbotSniper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener("on_message")
    async def slotbotsnipe(self, message: discord.Message):
        if message.author.id == 346353957029019648:
            if slotbot:
                if "Hurry and pick it up with" in message.content:
                    try:
                        start = time.time()
                        await message.channel.send("~grab")
                        end = time.time()
                        util.log(f"Sniped slotbot in guild [bold]{message.guild.name}[/bold], ID: [bold]{message.guild.id}[/bold]. ({math.floor((end - start) * 1000)} ms)")
                    except:
                        util.log(f"Failed to snipe slotbot in guild [bold]{message.guild.name}[/bold], ID: [bold]{message.guild.id}[/bold].", error=True)
                