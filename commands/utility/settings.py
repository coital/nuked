import os, discord, json, datetime, time
from discord.ext import commands
from modules import util

def setup(bot: commands.Bot):
    bot.add_cog(Settings(bot))

with open("./config.json") as f:
    config = json.load(f)
    
light_mode = config["Enable Light Mode"]
rich_presence = config["Discord Rich Presence"]
message_logger = config["Enable Mention Logger"]
mentionblocker = config["Enable Mention Blocker"]
disable_eval = config["Disable Eval Command"]
slotbot = config["Enable Slotbot Sniper"]
nitrosniper = config["Enable Nitro Sniper"]
default_prefix = config["Default Prefix"]
nitro_logger_enabled = config["Logging"]["Nitro Logger"] != ""

class Settings(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.command()
    async def settings(self, ctx):
        await ctx.message.delete()
        embed = discord.Embed(
                            title="Settings for Nuked", 
                            description="These are your settings from config.json.", 
                            color=0xFAFAFA, 
                            timestamp=datetime.datetime.utcfromtimestamp(time.time()))
        embed.add_field(name="**Light Mode**", value="on" if light_mode else "off", inline=True)
        embed.add_field(name="**Rich Presence**", value="on" if light_mode else "off", inline=True)
        embed.add_field(name="**Mention Logger**", value="on" if message_logger else "off", inline=True)
        #embed.add_field(name="‎", value="‎", inline=False)
        embed.add_field(name="**Block Mentions**", value="on" if mentionblocker else "off", inline=True)
        embed.add_field(name="**Disable Eval**", value="on" if disable_eval else "off", inline=True)
        embed.add_field(name="**Slotbot Sniper**", value="on" if slotbot else "off", inline=True)
        #embed.add_field(name="‎", value="‎", inline=False)
        embed.add_field(name="**Nitro Sniper**", value="on" if nitrosniper else "off", inline=True)
        embed.add_field(name="**Default Prefix**", value=default_prefix, inline=True)
        embed.add_field(name="**Nitro Logger (Webhook)**", value="on" if nitro_logger_enabled else "off", inline=True)
        embed.add_field(name="**Theme**", value="default (v6)", inline=True)
        await ctx.send(embed=embed, delete_after=20)
        
    