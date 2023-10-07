from threading import Thread

from .. import Forge


class modBase:
    def __init__(self, root: Forge, name, threadFunc):
        self.name = name
        if name not in root.modThreads:
            t = Thread(target=threadFunc)
            t.start()
            root.modThreads[name] = t

    def preRender(self, data):
        ...

    def postRender(self, data):
        ...

    def Fail(self, data, error):
        print(f"[ERROR-{self.name}]  : This item has failed to finish loading due to {error}; data PKG: {data}")

    def Success(self, data):
        print(f"[INFO-{self.name}]   : This item has successfully finished loading; data PKG: {data}")
