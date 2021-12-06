import os, json, time
from colorama import Fore
from modules import util

def init():
    if not os.path.exists("./config.json"):
            with open("./config.json", "w") as fp:
                print(Fore.LIGHTCYAN_EX +
                      "Welcome to the initial setup process for the Nuked selfbot.")
                setup_token = input("Enter your Discord token: ")
                setup_password = input(
                    "Enter your Discord password (enter \"None\" or nothing if you don\'t want to): ")
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
                    "Logging": {
                        "Mention Logger": "",
                        "Nitro Logger": "",
                        "Ghost Ping Logger": ""
                    }
                }
                json.dump(setup_data, fp, indent=4)
                print("Additional settings can be tweaked in config.json!")
                time.sleep(2)
            util.clear()
            print(Fore.RESET)
    else:
        pass