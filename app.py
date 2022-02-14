import json
from mainWindow import createMainWindow

if __name__ == "__main__":
    with open('mods.json', 'r') as f:
        mods = json.load(f)

    with open('inventory.json', 'r') as f:
        inventory = json.load(f)

    createMainWindow(mods, inventory, None)