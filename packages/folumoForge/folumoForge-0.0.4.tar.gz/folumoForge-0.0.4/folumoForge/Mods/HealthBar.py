from .. import Forge
from ..Items import Rect
from ..Items.base import itemBase
from ..Mods import modBase


def modThread(root, name):
    while root.Running:
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                mod = item.mods[name]
                mod.barMax.config((mod.item.xy[0]-(mod.maxHP/4), mod.item.xy[1] - 20), (mod.maxHP, 10))
                mod.barNow.config((mod.item.xy[0]-(mod.maxHP/4), mod.item.xy[1] - 20), (mod.HP, 10), "red")


class modHealthBar(modBase):
    def __init__(self, root: Forge, item: itemBase):
        super().__init__(root, "modHealthBar", lambda: modThread(root, "modHealthBar"))
        self.maxHP = 100
        self.HP = 10
        self.item = item
        self.barMax = Rect(item.screen, (self.item.xy[0]-(self.maxHP/4), self.item.xy[1]-20), (self.maxHP, 10))
        self.barNow = Rect(item.screen, (self.item.xy[0]-(self.maxHP/4), self.item.xy[1]-20), (self.HP, 10), "red")
