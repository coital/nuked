
import os, json, time
from modules import package

def init():
    from modules.util import clear, log, console, check_token, get_config, get_token
    import modules.util_detect_token as utd
    clear()
    if not os.path.exists("./config.json"):
        clear()
        log("Welcome to the initial setup process for the Nuked selfbot.")
        log("If you're updating, you can move your current config.json here and use that configuration.")
        log("Enter '1' if you would like to log in using your Discord credentials [bold](will not work with 2FA!)[/bold]", color="green")
        log("Enter '2' if you would like to log in using your Discord token.", color="green")
        log("Enter '3' if you would like Nuked to automatically detect Discord accounts [bold](Experimental)[/bold].", color="green")
        choice = console.input(f"\n>")
        match choice:
            case '1':
                with open("./config.json", "w") as fp:
                    clear()
                    setup_email = console.input("Enter your [bold]Discord email[/bold]: ")
                    setup_password = console.input("Enter your [bold]Discord password[/bold]: ")
                    token = get_token(setup_email, setup_password)
                    if token != None:
                        setup_data = {
                            "Auto Update": True,
                            "Discord Token": token,
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
                            "Disable Cog Load Message": True,
                            "Logging": {
                                "Nitro Logger": ""
                            }
                        }
                        json.dump(setup_data, fp, indent=4)
                        log("[bold]Additional settings can be tweaked in config.json![/bold]")
                        time.sleep(2)
                        check_token(setup_data["Discord Token"])
                    else:
                        log("The username and password combination was incorrect. Restarting..", error=True)
                        os.remove("config.json")
                        time.sleep(1)
                        package.restart()
            case '2':
                with open("./config.json", "w") as fp:
                    clear()
                    setup_token = console.input("Enter your [bold]Discord token[/bold]: ")
                    setup_password = console.input(
                        "Enter your [bold]Discord password[/bold] (enter [bold]None[/bold] or press the [bold]Enter[/bold] key if you don't want to): ")
                    if setup_password == "":
                        setup_password = "None"
                    setup_data = {
                        "Auto Update": True,
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
                        "Disable Cog Load Message": True,
                        "Logging": {
                            "Nitro Logger": ""
                        }
                    }
                    json.dump(setup_data, fp, indent=4)
                    log("[bold]Additional settings can be tweaked in config.json![/bold]")
                    time.sleep(2)
                    check_token(setup_data["Discord Token"])
            case '3':
                accounts = utd.detect_tokens()
                for item in accounts:
                    try:
                        utd.get_username(item)
                    except KeyError:
                        accounts.remove(item)
                if len(accounts) > 0:
                    print(f'\nItems found: {len(accounts)}')
                    print('Accounts:')
                    for item in accounts:
                        print(f'{utd.get_username(item)} -- {item[:24]}..')
                    num = console.input(f'\nOut of the {len(accounts)} tokens, which one would you like to log into?\n\n>')
                    slice = int(num)
                    slice = slice - 1
                    with open("./config.json", "w") as fp:
                        clear()
                        try:
                            setup_data = {
                                "Auto Update": True,
                                "Discord Token": accounts[slice],
                                "Discord Password": None,
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
                                "Disable Cog Load Message": True,
                                "Logging": {
                                    "Nitro Logger": ""
                                }
                            }
                            json.dump(setup_data, fp, indent=4)
                            log("[bold]Additional settings can be tweaked in config.json![/bold]")
                            time.sleep(2)
                            check_token(setup_data["Discord Token"])
                        except IndexError:
                            log("Token was out of the list index. Restarting.", color="red")
                            package.restart()
                else:
                    log("No tokens were found to log into. Restarting.", color="red")
                    package.restart()
            case _:
                package.restart()
        clear()
    else:
        if os.path.getsize(f"{os.getcwd()}/config.json") == 0:
            os.remove(f"{os.getcwd()}/config.json")
            package.restart()
        else:
            check_token(get_config()["Discord Token"])