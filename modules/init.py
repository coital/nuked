
import os, json, time, sys
from modules import package

try:
    from colorama import Fore
except ImportError as e:
    package.install_module(module=e.name)
    print(f"Installed missing module {e.name}, restarting..")
    package.restart()

def init():
    
    from modules.util import clear, log, console, check_token, get_config
    clear()
    if not os.path.exists("./config.json"):
        clear()
        with open("./config.json", "w") as fp:
            clear()
            log("Welcome to the initial setup process for the Nuked selfbot.")
            setup_token = console.input("Enter your [bold]Discord token[/bold]: ")
            setup_password = console.input(
                "Enter your [bold]Discord password[/bold] (enter [bold]None[/bold] or press the [bold]Enter[/bold] key if you don't want to): ")
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
            log("[bold]Additional settings can be tweaked in config.json![/bold]")
            time.sleep(2)
            check_token(setup_data["Discord Token"])
        clear()
    else:
        if os.path.getsize(f"{os.getcwd()}/config.json") == 0:
            os.remove(f"{os.getcwd()}/config.json")
            package.restart()
        else:
            check_token(get_config()["Discord Token"])