import os, subprocess, sys
from typing import List

def install_module(module: str=None, modules: List[str]=None):
    if not module and not modules:
        return
    elif modules:
        for module in modules:
            if "not found" in subprocess.getoutput(f"python -m pip show {module}"):
                os.system(f"python -m pip install {module}")
                print(f"Installed {module}")
            else:
                print(f"{module} already installed, continuing")
        print("Restarting.")
        os.system('python "' + os.getcwd() + "/" + sys.argv[0] + '"')
    elif module:
        if "not found" in subprocess.getoutput(f"python -m pip show {module}"):
            os.system(f"python -m pip install {module}")
            print(f"Installed {module}")
    return