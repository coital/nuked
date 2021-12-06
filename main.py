import discord, json, ctypes, time, cursor
from modules import util, init
from discord.ext import commands
init.init()

with open("./config.json") as f:
    config = json.load(f)

token = config["Discord Token"]
light_mode = config["Enable Light Mode"]
rich_presence = config["Discord Rich Presence"]

if rich_presence:
    util.setup_rich_presence()
# util.check_for_update()

try:
    cursor.hide()
except:
    pass

class Nuked(commands.Bot):
    async def on_connect(self):
        await self.change_presence(activity=None, status=discord.Status.dnd)
        for command in util.load_commands():
            self.load_extension(command)
            util.log(f"Loaded cog: {command}")
        time.sleep(1.5)
        
        util.clear()
        util.presplash()
        util.splash()
        util.log(f"{client.user.name}#{client.user.discriminator} was logged in.")
        if light_mode:
            ctypes.windll.kernel32.SetConsoleTitleW("Nuked - Enabling Light Mode")
            client.recursively_remove_all_commands()
            util.log("Light mode is enabled - commands will not work.")
        ctypes.windll.kernel32.SetConsoleTitleW(f"Nuked - {client.user.name}#{client.user.discriminator}")



client = Nuked(command_prefix=".", help_command=None, self_bot=True) 
client.run(token)
