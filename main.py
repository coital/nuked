
print("[status] loading package manager..")
from modules import package, util, init
print(f"[status] done loading package manager")

try:
    import time, math
    start = time.time()
    print("[status] loading main.py imports")
    import discord, json, ctypes, cursor, signal, sys
    from discord.ext import commands
    end = time.time()
    print(f"[status] done loading main.py imports ({math.ceil(end - start)} s)")
except ImportError as e:
    if "discord" in str(e):
        package.install_module(module="discord.py-self")
    else:
        package.install_module(module=e.name)
        print(f"Installed missing module {e.name}, restarting..")
    time.sleep(1.5)
    package.restart()


init.init()

util.sys.tracebacklimit = 0
with open("./config.json") as f:
    config = json.load(f)

token = config["Discord Token"]
light_mode = config["Enable Light Mode"]
rich_presence = config["Discord Rich Presence"]

if rich_presence:
    util.setup_rich_presence()

if util.os.name == "nt":
    package.install_module(module="win10toast")

# util.check_for_update()

try:
    cursor.hide()
except Exception as e:
    util.error(f"Exception while setting up cursor: [bold]{str(e)}[/bold]")

class Nuked(commands.Bot):
    async def on_connect(self):
        try:
            signal.signal(signal.SIGINT, util.signal_handler)
        except Exception as e:
            util.error(f"Error while setting up signal handler: {str(e)}")
        self.msgsniper = True
        self.snipe_history_dict = {}
        self.sniped_message_dict = {}
        self.sniped_edited_message_dict = {}
        await self.change_presence(activity=None, status=discord.Status.dnd)
        for command in util.load_commands():
            try:
                self.load_extension(command)
                util.log(f"Loaded cog: [bold]{command}[/bold]")
            except commands.errors.ExtensionFailed as e:
                # util.error(f"There was an extension exception in on_connect: [bold]{e.name}: {e.original}[/bold]") 
                if isinstance(e.original, ModuleNotFoundError):
                    util.error(f"Missing module: [bold]{e.original.name}[/bold]. Attempting to install it.")
                    package.install_module(module=e.original.name)
                    package.restart()
            except Exception as e:
                util.error(f"There was an exception in on_connect: [bold]{e}[/bold]")
        time.sleep(1.5)
        util.clear()
        util.presplash()
        util.splash()
        util.toast_message(f"{self.user.name}#{self.user.discriminator} was logged in.")
        util.log(f"[bold]{self.user.name}#{self.user.discriminator}[/bold] was logged in.")
        if light_mode:
            util.set_title("Nuked - Enabling Light Mode")
            for command in util.enable_light_mode():
                self.unload_extension(command)
            util.log("Light mode is enabled - commands will not work.")
        else:
            util.log(f"Loaded [bold]{util.load_commands().__len__()}[/bold] cogs.")
        util.set_title(f"Nuked - {self.user.name}#{self.user.discriminator}")


Nuked(command_prefix=".", help_command=None, self_bot=True).run(token)
