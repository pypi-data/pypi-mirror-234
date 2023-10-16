from . import Screen
from ..Mods import modBase


class itemBase:
    mods = {}
    screen: Screen = None
    xy = (0, 0)
    wh = ()
    color = "blue"

    def delete(self):
        for item in self.screen.Items:
            if item == self:
                self.screen.Items.remove(self)

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        pass
