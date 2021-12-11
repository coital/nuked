import discord, json, ctypes, time, cursor, signal, sys
from modules import util, init
from discord.ext import commands
init.init()
sys.tracebacklimit = 0
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
    signal.signal(signal.SIGINT, util.signal_handler)
except:
    pass

class Nuked(commands.Bot):
    async def on_connect(self):
        self.msgsniper = True
        self.snipe_history_dict = {}
        self.sniped_message_dict = {}
        self.sniped_edited_message_dict = {}
        await self.change_presence(activity=None, status=discord.Status.dnd)
        for command in util.load_commands():
            self.load_extension(command)
            util.log(f"Loaded cog: {command}")
        time.sleep(1.5)
        util.clear()
        util.presplash()
        util.splash()
        util.log(f"{self.user.name}#{self.user.discriminator} was logged in.")
        if light_mode:
            util.set_title("Nuked - Enabling Light Mode")
            for command in util.enable_light_mode():
                self.unload_extension(command)
            util.log("Light mode is enabled - commands will not work.")
        util.set_title(f"Nuked - {self.user.name}#{self.user.discriminator}")



Nuked(command_prefix=".", help_command=None, self_bot=True).run(token)
