import discord, datetime, time, aiohttp, random, base64
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Token(bot))

class Token(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
        self.languages = {
            'da'    : 'Danish, Denmark',
            'de'    : 'German, Germany',
            'en-GB' : 'English, United Kingdom',
            'en-US' : 'English, United States',
            'es-ES' : 'Spanish, Spain',
            'fr'    : 'French, France',
            'hr'    : 'Croatian, Croatia',
            'lt'    : 'Lithuanian, Lithuania',
            'hu'    : 'Hungarian, Hungary',
            'nl'    : 'Dutch, Netherlands',
            'no'    : 'Norwegian, Norway',
            'pl'    : 'Polish, Poland',
            'pt-BR' : 'Portuguese, Brazilian, Brazil',
            'ro'    : 'Romanian, Romania',
            'fi'    : 'Finnish, Finland',
            'sv-SE' : 'Swedish, Sweden',
            'vi'    : 'Vietnamese, Vietnam',
            'tr'    : 'Turkish, Turkey',
            'cs'    : 'Czech, Czechia, Czech Republic',
            'el'    : 'Greek, Greece',
            'bg'    : 'Bulgarian, Bulgaria',
            'ru'    : 'Russian, Russia',
            'uk'    : 'Ukranian, Ukraine',
            'th'    : 'Thai, Thailand',
            'zh-CN' : 'Chinese, China',
            'ja'    : 'Japanese',
            'zh-TW' : 'Chinese, Taiwan',
            'ko'    : 'Korean, Korea'
        }

    @commands.command()
    async def token(self, ctx, option: str=None, token: str = None):
        await ctx.message.delete()
        embed = discord.Embed(
                                title=f"**Token Tools**", color=util.get_color(), 
                                description=f"Tools to interact with Discord tokens", 
                                timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**View Information**", value=f"to view information on a Discord token, use `{self.client.command_prefix}token info <token>`.", inline=False)
        embed.add_field(name="**Locking a Token**", value=f"to lock a Discord token, use `{self.client.command_prefix}token lock <token>`.", inline=False)
        embed.add_field(name="**Generating a Token**", value=f"to generate a Discord token, use `{self.client.command_prefix}token generate`.", inline=False)
        if not option:
            await ctx.send(util.embed_to_str(embed), delete_after=20)
        else:
            match option:
                case "info":
                    headers = {
                        'Authorization': token,
                        'Content-Type': 'application/json'
                    }
                    async with aiohttp.ClientSession(headers=headers) as session:
                        async with session.get(f"{util.get_utd_api_link()}/users/@me/") as response:
                            if response.ok:
                                res_json = await response.json()
                                tag = f'{res_json["username"]}#{res_json["discriminator"]}'
                                id = res_json['id']
                                aid = res_json['avatar']
                                aurl = f'https://cdn.discordapp.com/avatars/{id}/{aid}.gif'
                                phone = res_json['phone']
                                email = res_json['email']
                                mfa = res_json['mfa_enabled']
                                flags = res_json['flags']
                                locale = res_json['locale']
                                verified = res_json['verified']
                                language = self.languages.get(locale)
                                nitro = False
                                embed = discord.Embed(title="**Token Information**",
                                            color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                                embed.set_thumbnail(url=aurl)
                                embed.add_field(name="**Tag**", value=f"{tag}", inline=False)
                                embed.add_field(name="**ID**", value=f"{id}", inline=False)
                                embed.add_field(name="**Email**", value=f"{email}", inline=False)
                                embed.add_field(name="**Phone Number**", value=f"{phone}", inline=False)
                                embed.add_field(name="**MFA Enabled?**", value=f"{mfa}", inline=False)
                                embed.add_field(name="**Language**", value=f"{language}", inline=False)
                                embed.add_field(name="**Has Nitro?**", value=f"{nitro}", inline=False)
                                embed.add_field(name="**Verified?**", value=f"{verified}", inline=False)
                            
                                await ctx.send(util.embed_to_str(embed), delete_after=25)
                            else:
                                await ctx.send(f"invalid token, response code {response.status}", delete_after=10)
                case "generate":
                    fh = ''.join((random.choices("1234567890", k=18)))
                    token = base64.b64encode(bytes(fh, 'utf-8')).decode() + '.X' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz' +
                                                                                          "1234567890", k=5)) + '.' + ''.join(random.choices('ABCDEFGHIJKLMNOPQRSTUVWXYZabcdefghijklmnopqrstuvwxyz-_' + "1234567890", k=27))
                    embed = discord.Embed(title="**Discord Token**", description="note: this token likely does not belong to an actual account.", 
                                          color=util.get_color(), timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.add_field(name="**Token**", value=f"{token}")
                    await ctx.send(util.embed_to_str(embed), delete_after=20)
                    
    