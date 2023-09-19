import discord, datetime, random, requests, asyncio, re
from discord.ext import commands
from modules import util
from bs4 import BeautifulSoup
import collections
collections.Callable = collections.abc.Callable
async def setup(bot: commands.Bot):
    await bot.add_cog(Blacktea(bot))
substr = "**"



def get_word(letters: str) -> str:
    if len(letters) <= 3:
        r = requests.get(f"https://wordfind.com/contains/{letters}")
        if r.status_code == 200:
            soup = BeautifulSoup(r.content, 'html.parser')
            html = soup.find("section")
            words = html.find_all("li", class_="dl")
            word = str(random.choice(words).get_text())
            result = ''.join([i for i in word if not i.isdigit()])
            return result
class Blacktea(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.fmsgwait = 1.35
        self.playing = False
    @commands.command(aliases=["bt"])
    async def blacktea(self, ctx: commands.context.Context, option: str = None, fmsgwait: float = 1.35):
        await ctx.message.delete()
        if not option:
            embed = discord.Embed(
                    title=f"**Automated Blacktea**", color=util.get_color(), 
                    description=f"Automatically play blacktea when enabled\nCurrent status: {'`enabled`' if self.playing else '`disabled`'}.", 
                    timestamp=datetime.datetime.utcfromtimestamp(util.time.time()))
            embed.add_field(name="**Enabling**", value=f"to enable automated blacktea, use `{self.client.command_prefix}blacktea on`.", inline=False)
            embed.add_field(name="**Disabling**", value=f"to disable automated blacktea, use `{self.client.command_prefix}blacktea off`.", inline=False)
            embed.add_field(name="**Setting timeout between message send and reaction check**", value=f"to set the timeout wait time between the message send and the reaction check/loop, use `{self.client.command_prefix}blacktea fmsg <limit>`.", inline=False)
            await ctx.send(util.embed_to_str(embed), delete_after=25)
        else:
            match option.lower():
                case "on":
                    self.playing = True
                case "off":
                    self.playing = False
                case "fmsgwait":
                    self.fmsgwait = fmsgwait
                case "fmsg":
                    self.fmsgwait = fmsgwait
                case "checkwait":
                    await ctx.send(self.fmsgwait, delete_after=25)
        def check(reaction, user):
            return user.id in [593921296224747521, 432610292342587392]
        while self.playing:
            async for message in ctx.channel.history(limit=1):
                if message.author.id in [593921296224747521, 432610292342587392]:
                    if self.client.user.mentioned_in(message):
                        if message.embeds:
                            embed1 = message.embeds[0]
                            if len(embed1.description) < 120:
                                reacted_to = False
                                val = -1
                                for i in range(0, 3):
                                    val = embed1.description.find("**", val + 1)
                                letters = embed1.description[val+2:]
                                letters = letters.replace("**.", "")
                                await asyncio.sleep(0.8)
                                while reacted_to == False:
                                    msg = await ctx.send(get_word(letters))
                                    await asyncio.sleep(1.25)
                                    reactions = (await ctx.channel.fetch_message(msg.id)).reactions
                                    for r in reactions:
                                        if str(r.emoji) == "✅":
                                            reacted_to = True
                                            break
                        elif "word containing:" in message.content:
                            reacted_to = False
                            val = -1
                            for i in range(0, 3):
                                val = message.content.find("**")
                            letters = message.content[val+2:]
                            letters = letters.replace("**", "")
                            while reacted_to == False:
                                async with ctx.typing():
                                    msg = await ctx.send(get_word(letters))
                                await asyncio.sleep(self.fmsgwait)
                                reactions = (await ctx.channel.fetch_message(msg.id)).reactions
                                for r in reactions:
                                    if str(r.emoji) == "✅":
                                        reacted_to = True
                                        break
                            await asyncio.sleep(0.055)

