from .base import modBase
from .. import Forge


def modThread(root: Forge, name: str):
    while root.Running:
        modItems = []
        for item in root.Screens[root.Screen].Items:
            if name in item.mods and "modGravity" in item.mods:
                modItems.append(item)

        for modI in modItems:
            modGravity = modI.mods["modGravity"]
            for modI2 in modItems:
                # Check if modI is touching modI2
                if (modI is not modI2 and
                        modI.xy[0] < modI2.xy[0] + modI2.wh[0] and
                        modI.xy[0] + modI.wh[0] > modI2.xy[0] and
                        modI.xy[1] < modI2.xy[1] + modI2.wh[1] and
                        modI.xy[1] + modI.wh[1] > modI2.xy[1]):
                    # Set modI's gravity Anchor to True and reset velocity
                    modGravity.Anchor = True
                    modGravity.velocity_x = 0.0
                    modGravity.velocity_y = 0.0

                else:
                    modGravity.Anchor = False


class modCollision(modBase):
    def __init__(self, root: Forge):
        super().__init__(root, "modCollision", lambda: modThread(root, "modCollision"))
