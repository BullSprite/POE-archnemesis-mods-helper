from tkinter import *

from cv2 import split
from recipe import Recipe
from treelib import Tree

#TODO: implement lootfilter change based on needed mods

#TODO: also add support for recipes of several mods in one time

def changeFilter(mods, finalized):
    filter_text = """Show # $type->exotic->archnemesis $tier->reagents
	ArchnemesisMod {0}
	Class "Archnemesis Mod"
	SetFontSize 40
	SetTextColor 200 0 250 255
	SetBorderColor 0 0 0 255
	SetBackgroundColor 0 0 0 255
	PlayAlertSound 3 300
	PlayEffect {1}
	MinimapIcon 1 {1} Pentagon
    """

    green = []
    red = []

    for mod in mods:
        if mod == "Empty" or mods[mod]['recipe'] is not None:
            continue
        if mod not in finalized:
            green.append(f'"{mod}"')
        else:
            red.append(f'"{mod}"')

    path = r""

    with open(path, "r") as f:
        lines = f.readlines()
    
    for i in range(len(lines) - 1, -1, -1):
        if lines[i] == "Show # $type->exotic->archnemesis $tier->reagents":
            lines = lines[:i] + lines[i+10:]

    lines += filter_text.format(' '.join(green), 'Green') + filter_text.format(' '.join(red), 'Red')
    with open(path, "w") as f:
        f.write(''.join(lines))



def createTree(recipe, tree, idx, pidx):
    if idx == 0:
        tree.create_node(str(recipe), 0)
    else:
        tree.create_node(str(recipe), idx, pidx)
    i = 1
    if recipe.recipe is None:
        return
    if not recipe.available:
        for rec in recipe.recipe:
            createTree(rec, tree, (idx + i) * 10, idx)
            i += 1

def textCreation(textField, recipe, mods):
    if recipe.recipe:
        tree = Tree()

        createTree(recipe, tree, 0, 0)
        textField.insert('end', str(tree))

    fin = recipe.finalize(mods={}) 
    #changeFilter(mods, fin)
    if not fin:
        if not recipe.recipe:
            if mods[recipe]['location']:
                textField.insert('end', f"You can find this mod in next locations: {', '.join(mods[recipe]['location'])}")
            else:
                textField.insert('end', "No info about locations")
        else:
            textField.insert('end', f"You already have this mode")
    else:
        for mod in fin:
            textField.insert('end', f"You need {fin[mod]} {mod}. ")
            if mods[mod]['location']:
                textField.insert('end', f"You can find it on next locations: {', '.join(mods[mod]['location'][:3])}.")
                if len(mods[mod]['location']) > 3:
                    textField.insert('end', f"\nFor more locations information look recipe for {mod}.")
            textField.insert('end', '\n')
    del(recipe)

        

def createRecipeWindow(main, mod, mods, inventory):
    recipe = Recipe(mod, mods, inventory)

    root = Toplevel(main)
    # options = {'font': (None, 12)}
    root['bg'] = '#fafafa'
    root.title(f'Your recipe for {mod}')
    
    textField = Text(root)
    textCreation(textField, recipe, mods)
    textField.configure(state='disabled')
    textField.pack()

    root.resizable(width=False, height=False)
    root.mainloop()