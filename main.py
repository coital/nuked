print("[status] initializing..")
from modules import package, util, init
import sys
if sys.version_info < (3, 10):
    print("This selfbot requires Python 3.10.")
    input()
    exit()
util.check_for_update()
print("[status] loading package manager..")
print(f"[status] done loading package manager")
try:
    import time, math
    start = time.time()
    print("[status] loading main.py imports")
    import discord, cursor, signal, sys
    from discord.ext import commands
    end = time.time()
    print(f"[status] done loading main.py imports ({math.ceil(end - start)} s)")
except ImportError as e:
    if "discord" in str(e):
        package.install_module(module="discord.py-self")
    else:
        package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
    package.restart()

if util.os.name == "nt":
    package.install_module(module="win10toast")

init.init()
util.sys.tracebacklimit = 0
config = util.get_config()
token = config["Discord Token"]
light_mode = config["Enable Light Mode"]
rich_presence = config["Discord Rich Presence"]
disable_cog_message = config["Disable Cog Load Message"]

if rich_presence:
    util.setup_rich_presence()
try:
    cursor.hide()
except Exception as e:
    util.log(f"Exception while setting up cursor: [bold]{str(e)}[/bold]", error=True)

class Nuked(commands.Bot):
    async def on_connect(self):
        try:
            signal.signal(signal.SIGINT, util.signal_handler)
        except Exception as e:
            util.log(f"Error while setting up signal handler: {str(e)}", error=True)
        self.msgsniper = True
        self.snipe_history_dict = {}
        self.sniped_message_dict = {}
        self.sniped_edited_message_dict = {}
        await self.change_presence(activity=None, status=discord.Status.dnd)
        if disable_cog_message:
            util.log("Loading..")
        for command in util.load_commands():
            try:
                self.load_extension(command)
                if not disable_cog_message:
                    util.log(f"Loaded cog: [bold]{command}[/bold].\n")
            except commands.errors.ExtensionFailed as e:
                if isinstance(e.original, ModuleNotFoundError):
                    util.log(f"Missing module: [bold]{e.original.name}[/bold]. Attempting to install it.", error=True)
                    package.install_module(module=e.original.name)
                    package.restart()
            except Exception as e:
                util.log(f"There was an exception in on_connect: [bold]{e}[/bold]", error=True)
        time.sleep(1.5)
        util.clear()
        util.presplash()
        util.splash()
        if light_mode:
            for command in util.enable_light_mode():
                self.unload_extension(command)
            util.log("Light mode is enabled - commands [bold]will not[/bold] work.")
        util.set_title(f"Nuked - {self.user.name}#{self.user.discriminator}")
        util.log(f"[bold]{self.user.name}#{self.user.discriminator}[/bold] was logged in.")
        util.toast_message(f"{self.user.name}#{self.user.discriminator} was logged in.")


Nuked(command_prefix=".", help_command=None, self_bot=True).run(token)
