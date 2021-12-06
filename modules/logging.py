import discord, os, aiohttp, json, datetime, time

from discord.webhook import AsyncWebhookAdapter, RequestsWebhookAdapter
from modules import util

with open("./config.json") as f:
    config = json.load(f)

nitro_logging = config.get["Logging"]["Nitro Logger"]


async def send_data(data: str = None, category: str = None):
    if not data:
        return
    else:
        match category:
            case "nitro":
                if nitro_logging == "":
                    return
                async with aiohttp.ClientSession() as session:
                    embed = discord.Embed(title="**Nuked | Nitro**", color=0xFAFAFA, timestamp=datetime.datetime.utcfromtimestamp(time.time()))
                    embed.add_field(name="**Data**", value=data)
                    webhook = discord.Webhook.from_url(url=nitro_logging, adapter=AsyncWebhookAdapter(session))
                    await webhook.send(
                        username="Nuked", 
                        avatar_url="https://cdn.discordapp.com/attachments/820836670857412710/820946025799745576/avatar.png",
                        embed=embed)
            case None:
                return
        
    