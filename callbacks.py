from tkinter import messagebox
from recipeWindow import createRecipeWindow
from scanWindow import  createScanWindow
from cv2 import imwrite

def getWidget(func):
    def wrapper(*args, **kwargs):
        for arg in kwargs:
            if arg != 'main' and hasattr(kwargs[arg], '__call__'):
                kwargs[arg] = kwargs[arg]()
        func(*args, **kwargs)
    return wrapper

def checkMod(mod, mods):
    if not mod in mods:
        messagebox.showerror(title="Error!", message="No such mod!")
        return False
    return True

@getWidget
def recipeCallBack(*args, main, mod, mods, inventory, **kwargs):
    if checkMod(mod, mods):    
        createRecipeWindow(main, mod, mods, inventory)

@getWidget
def scanCallBack(*args, main, mods, inventory, **kwargs):
    createScanWindow(main, mods, inventory)
