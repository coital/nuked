
import os, json, time, sys
from modules import package

try:
    from colorama import Fore
except ImportError as e:
    package.install_module(module=e.name)
    print(f"Installed missing module {e.name}, restarting..")
    package.restart()

def init():
    from modules import util
    util.clear()
    if util.sys.version_info < (3, 10):
        util.log("This selfbot requires [bold]Python 3.10[/bold].")
        input()
        exit()
    if not os.path.exists("./config.json"):
        util.clear()
        with open("./config.json", "w") as fp:
            util.clear()
            util.log("Welcome to the initial setup process for the Nuked selfbot.")
            setup_token = input("Enter your Discord token: ")
            setup_password = input(
                "Enter your Discord password (enter \"None\" or nothing if you don't want to): ")
            if setup_password == "":
                setup_password = "None"
            setup_data = {
                "Discord Token": setup_token,
                "Discord Password": setup_password,
                "Discord Rich Presence": True,
                "Default Prefix": ".",
                "Enable Mention Logger": True,
                "Enable Mention Blocker": False,
                "Enable Light Mode": False,
                "Disable Eval Command": False,
                "Enable Slotbot Sniper": True,
                "Enable Nitro Sniper": True,
                "Automatically Check for Updates": True,
                "Random Splash Color": False,
                "Theme": "Default",
                "Logging": {
                    "Nitro Logger": ""
                }
            }
            json.dump(setup_data, fp, indent=4)
            util.log("[bold]Additional settings can be tweaked in config.json![/bold]")
            time.sleep(2)
            util.check_token(setup_data["Discord Token"])
        util.clear()
    else:
        if os.path.getsize(f"{os.getcwd()}/config.json") == 0:
            os.remove(f"{os.getcwd()}/config.json")
            package.restart()
        else:
            util.check_token(util.get_config()["Discord Token"])