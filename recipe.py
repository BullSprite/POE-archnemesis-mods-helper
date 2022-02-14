class Recipe:
    def __init__(self, name, mods, inventory):
        self.name = name
        self.recipe = self.__getItems(mods, inventory)
        self.available = self.__useFromInventory(inventory)

    def __str__(self):
        return self.name + ("" if self.available else " (need)")

    def __repr__(self) -> str:
        return self.name

    def __hash__(self) -> int:
        return hash(self.name)

    def __eq__(self, __o: object) -> bool:
        return self.name == __o

    def __useFromInventory(self, inventory):
        if inventory[self.name] == 0:
            return False
        inventory[self.name] -= 1
        return True

    def __getItems(self, mods, inventory):
        if mods[self.name]['recipe'] == None:
            return None
        return [Recipe(name, mods, inventory) for name in mods[self.name]['recipe']]

    def finalize(self, mods={}, is_first=True):
        if self.recipe is None:
            if not self.available:
                if self.name not in mods:
                    mods[self.name] = 1
                else:
                    mods[self.name] += 1
            return
        for mod in self.recipe:
            mod.finalize(mods, False)
        if is_first:
            return mods 

    def getRecipe(self):
        ...
