from time import sleep

from .. import Forge
from ..Mods.base import modBase


def modThread(root: Forge, name):
    while root.Running:
        for item in root.Screens[root.Screen].Items:
            if name in item.mods:
                mod = item.mods[name]
                if not mod.Anchor:
                    dTime = root.delta_time / 1000

                    if mod.side == "down":
                        mod.velocity_y += mod.gravity_acceleration * dTime
                    elif mod.side == "up":
                        mod.velocity_y -= mod.gravity_acceleration * dTime
                    elif mod.side == "left":
                        mod.velocity_x -= mod.gravity_acceleration * dTime
                    elif mod.side == "right":
                        mod.velocity_x += mod.gravity_acceleration * dTime
                    elif mod.side == "left-down":
                        mod.velocity_x -= mod.gravity_acceleration * dTime
                        mod.velocity_y += mod.gravity_acceleration * dTime
                    elif mod.side == "left-up":
                        mod.velocity_x -= mod.gravity_acceleration * dTime
                        mod.velocity_y -= mod.gravity_acceleration * dTime
                    elif mod.side == "right-down":
                        mod.velocity_x += mod.gravity_acceleration * dTime
                        mod.velocity_y += mod.gravity_acceleration * dTime
                    elif mod.side == "right-up":
                        mod.velocity_x += mod.gravity_acceleration * dTime
                        mod.velocity_y -= mod.gravity_acceleration * dTime

                    item.xy = (item.xy[0] + mod.velocity_x, item.xy[1] + mod.velocity_y)
                    sleep(dTime)


class modGravity(modBase):
    def __init__(self, root: Forge):
        super().__init__(root, "modGravity", lambda: modThread(root, "modGravity"))
        self.Anchor = False
        self.velocity_x = 0.0
        self.velocity_y = 0.0
        self.side = "down"
        self.gravity_acceleration = 9.81
