import discord, json, re, time, aiohttp, math
from colorama import Fore, Style
from discord.ext import commands
from modules import util
from modules import logging

with open("./config.json") as f:
    config = json.load(f)

def setup(bot: commands.Bot):
    bot.add_cog(NitroSniper(bot))

nitrosniper = config["Enable Nitro Sniper"]
token = config["Discord Token"]

class NitroSniper(commands.Cog):
    def __init__(self, bot: commands.Bot):
        self.client = bot
    @commands.Cog.listener("on_message")
    async def _(self, message: discord.Message):
        if "discord.gift/" in message.content:
            if nitrosniper:
                code = re.search("discord.gift/(.*)", message.content).group(1)
                start = time.time()
                if len(code) < 16:
                    end = time.time()
                    print(Fore.CYAN + f"\n[{util.get_time()}] {Fore.RESET}A fake nitro code sent by user {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {Fore.RED}{code}{Fore.RESET}. ({math.floor((end - start) * 1000)} ms)")
                    return
                async with aiohttp.ClientSession(headers={"authorization": token, "user-agent": "Mozilla/5.0"}) as session:
                    async with session.post(url="https://discord.com/api/v9/entitlements/gift-codes/{code}/redeem", json={"channel_id": message.channel.id}) as response:
                        end = time.time()
                        text = await response.text()
                        if "This gift has been redeemed already." in text:
                            print(
                                Fore.CYAN + f"\n[{util.get_time()}] {Fore.RESET}A redeemed nitro code sent by user {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {Fore.LIGHTRED_EX}{code}{Fore.RESET}. ({math.floor((end - start) * 1000)} ms)")
                            await logging.send_data(f"[{util.get_time()}] A redeemed nitro code sent by user {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {code}. ({math.floor((end - start) * 1000)} ms)", "nitro")
                        elif "subscription_plan" in text:
                            print(
                                Fore.CYAN + f"\n[{util.get_time()}] {Fore.RESET}A valid nitro code sent by {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {Fore.LIGHTGREEN_EX}{code}{Fore.RESET}. ({math.floor((end - start) * 1000)} ms)")
                            await logging.send_data(f"\n[{util.get_time()}] A valid nitro code sent by {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {code}. ({math.floor((end - start) * 1000)} ms)", "nitro")
                            util.toast_message(f"Successfully claimed a nitro code sent by {message.author}.")
                        elif "Unknown Gift Code" in text:
                            print(
                                Fore.CYAN + f"\n[{util.get_time()}] {Fore.RESET}An invalid nitro code sent by {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {Style.DIM}{code}{Style.RESET_ALL}. ({math.floor((end - start) * 1000)} ms)")
                            await logging.send_data(f"\n[{util.get_time()}] An invalid nitro code sent by {message.author} in {message.guild.name if message.guild else 'DMs'} was sniped: {code}. ({math.floor((end - start) * 1000)} ms)", "nitro")
                        else:
                            print(
                                Fore.CYAN + f"\n[{util.get_time()}] {Fore.RESET}An unknown error occurred when sniping the code sent by {message.author} in {message.guild.name if message.guild else 'DMs'}: {Style.DIM}{code}{Style.RESET_ALL}. ({math.floor((end - start) * 1000)} ms)")
                            print(text)
                        await session.close()
                