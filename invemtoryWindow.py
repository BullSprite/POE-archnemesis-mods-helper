from tkinter import *

def createInventoryWindow():
    root = Tk()
    # options = {'font': (None, 12)}
    root['bg'] = '#fafafa'
    root.title(f'Inventory')

    textField = Text(root)
    saveButton = Button()
