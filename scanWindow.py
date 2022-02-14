from tkinter import *
from tkinter import messagebox
from ttkwidgets.autocomplete import AutocompleteCombobox
from functools import partial
from capture import capture
from PIL import Image, ImageTk
from cv2 import imwrite, cvtColor, COLOR_RGB2BGR

def checkMod(mod, mods):
    if not mod in mods:
        messagebox.showerror(title="Error!", message="No such mod!")
        return False
    return True

def saveCallBack(*args, main, mods, inventory, entries, screen, **kwargs):
    local_inventory = inventory.copy()
    for mod in local_inventory:
        local_inventory[mod] = 0
    for entry, mod in zip(entries, screen):
        name = entry.get()
        if not checkMod(name, mods):
            return
        local_inventory[name] += 1
        if name != mod[0]:
            imwrite(f'picturedb\\{name}.png', cvtColor(mod[1][:38,:52], COLOR_RGB2BGR))
    for key in inventory:
        inventory[key] = local_inventory[key]
    main.destroy()

def createScanWindow(main, mods, inventory):
    root = Toplevel(main)
    root['bg'] = '#fafafa'
    root.title('Inventory')
    root.attributes('-topmost', True)

    inv = capture()
    labels = []
    entries = [AutocompleteCombobox(root, completevalues=mods, width=8) for i in range(64)]
    for i in range(8):
        for j in range(8):
            image = ImageTk.PhotoImage(Image.fromarray(inv[i*8 + j][1]).resize((40, 40), Image.ANTIALIAS))
            label =  Label(root, image = image)
            label.image = image
            label.grid(row=i*2, column=j)
            labels.append(label)
            entries[i*8 + j].grid(row=i*2 + 1, column=j)
            entries[i*8 + j].insert(END, inv[i*8 + j][0])
    saveButton = Button(root, text="Save",command=partial(saveCallBack,
                                                         main=root,
                                                         mods=mods,
                                                         inventory=inventory,
                                                         entries=entries,
                                                         screen=inv))
    saveButton.grid(row=16, columnspan=8, sticky='nswe')
    root.resizable(width=False, height=False)
    root.mainloop()
