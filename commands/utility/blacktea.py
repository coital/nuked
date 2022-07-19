import discord, datetime, random, requests, asyncio
from discord import Embed
from discord.embeds import EmbedProxy
from discord.ext import commands
from modules import util
from bs4 import BeautifulSoup

def setup(bot: commands.Bot):
    bot.add_cog(Blacktea(bot))
substr = "**"
global playing
playing = False


def get_word(letters: str) -> str:
    if len(letters) <= 3:
        r = requests.get(f"https://wordfind.com/contains/{letters}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            html = soup.find("section")
            words = html.find_all("li", class_="dl")
            return str(random.choice(words).get_text())[:-2]

class Blacktea(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def blacktea(self, ctx, option: str = None):
        await ctx.message.delete()
        if not option:
            embed = discord.Embed(
                    title=f"**Automated Blacktea**", color=util.get_color(), 
                    description=f"Automatically play blacktea when enabled", 
                    timestamp=datetime.datetime.utcfromtimestamp(util.time.time()))
            embed.add_field(name="**Enabling**", value=f"to enable automated blacktea `{self.client.command_prefix}blacktea on`.", inline=False)
            embed.add_field(name="**Disabling**", value=f"to disable automated blacktea `{self.client.command_prefix}blacktea off`.", inline=False)
            await ctx.send(util.embed_to_str(embed), delete_after=25)
        else:
            match option.lower():
                case "on":
                    playing = True
                case "off":
                    playing = False

        while playing:
            messages = await ctx.channel.history(limit=1).flatten()
            for message in messages:
                if message.author.id in [593921296224747521, 432610292342587392]:
                    if self.client.user.mentioned_in(message):
                        if message.embeds:
                            embed1 = message.embeds[0]
                            if len(embed1.description) < 120:
                                val = -1
                                for i in range(0, 3):
                                    val = embed1.description.find("**", val + 1)
                                letters = embed1.description[val+2:]
                                letters = letters.replace("**.", "")
                                await asyncio.sleep(0.5)
                                await ctx.send(get_word(letters))
                        elif message.content.find("Type a word"):
                                val = -1
                                for i in range(0, 3):
                                    val = message.content.find("**")
                                letters = message.content[val+2:]
                                letters = letters.replace("**", "")
                                await asyncio.sleep(0.7)
                                await ctx.send(get_word(letters))
                        await asyncio.sleep(1)

