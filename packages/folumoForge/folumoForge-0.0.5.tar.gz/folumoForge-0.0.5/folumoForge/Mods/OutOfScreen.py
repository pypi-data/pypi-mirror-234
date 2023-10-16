from time import sleep

import pygame

from .. import Forge
from ..Mods.base import modBase


def modThread(root: Forge, name):
    while root.Running:
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                mod = item.mods[name]
                root = item.screen.root
                if item.xy[1] >= root.wh[1]:  # down
                    item.xy = (item.xy[0], 0)

                elif item.xy[1]+item.wh[1] < 0:  # up
                    item.xy = (item.xy[0], root.wh[1]-item.wh[1])

                elif item.xy[0] > root.wh[0]:  # right
                    item.xy = (0, item.xy[0])

                elif item.xy[0] + item.wh[0] < 0:  # left
                    item.xy = (root.wh[0] - item.wh[0], item.xy[1])


class modOutOfScreenTP(modBase):
    def __init__(self, root: Forge):
        super().__init__(root, "modOutOfScreenTP", lambda: modThread(root, "modOutOfScreenTP"))
