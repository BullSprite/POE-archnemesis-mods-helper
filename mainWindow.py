from tabnanny import check
from ttkwidgets.autocomplete import AutocompleteCombobox
from tkinter import *
from functools import partial
from callbacks import recipeCallBack, scanCallBack
import keyboard
import json

def onClose(main, inventory):
    main.destroy()
    with open("inventory.json", 'w') as f:
        json.dump(inventory, f, indent=4)
        
def changeButton(*args, button, **kwargs):
    button.invoke()

def createMainWindow(mods, inventory, locations):
    modsList = list(mods.keys())

    root = Tk()
    root.protocol("WM_DELETE_WINDOW", partial(onClose, main=root, inventory=inventory))
    root.attributes('-topmost', True)
    # root.update()
    options = {'font': (None, 12)}
    root['bg'] = '#fafafa'
    root.title('Mod crafter')
    root.geometry('425x275+1080+250')
    root.resizable(width=False, height=False)

    canvas = Canvas(root, height=275, width=425)
    canvas.pack()

    frame = Frame(root)
    frame.place(relwidth=1, relheight=1)

    title = Label(frame, text='Mods to create:', **options)
    title.place(x = 0, y = 30)
    bar = AutocompleteCombobox(frame, completevalues=modsList, **options)
    bar.place(x = 115, y = 30)
    bar.bind('<Return>', partial(recipeCallBack, 
                                 main=root, 
                                 mod=bar.get, 
                                 mods=mods, 
                                 inventory=inventory.copy))
    sButton = Button(frame, text="View recipe", command=partial(recipeCallBack,
                                                                main=root,
                                                                mod=bar.get,
                                                                mods=mods,
                                                                inventory=inventory.copy), **options)
    sButton.place(x = 320, y = 26)

    invButton = Button(frame, text="Scan", command=partial(scanCallBack,
                                                           main=root,
                                                           mods=modsList,
                                                           inventory=inventory), **options)
    invButton.place(x = 110, y = 137, width=200, height=100)

    keyboard.on_press_key("'", lambda _: invButton.invoke())

    root.mainloop()

