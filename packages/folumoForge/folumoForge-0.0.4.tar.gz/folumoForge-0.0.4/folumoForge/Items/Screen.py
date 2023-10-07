import pygame

from .. import Forge


class Screen:
    def __init__(self, root, name, size, title, fullScreen):
        self.title = title
        self.press = {}
        self.fullScreen = fullScreen
        self.root: Forge = root
        self.name = name
        self.size = size
        self.EventAble = []
        self.Items = []
        self.OnF = {}

    def SwitchScreen(self):
        if self.fullScreen:
            self.root.MainRoot = pygame.display.set_mode(self.size, pygame.FULLSCREEN)
        else:
            self.root.MainRoot = pygame.display.set_mode(self.size)

        pygame.display.set_caption(self.title)

        self.root.Screen = self.name

    def BindKey(self, unicodeID, func):
        self.press[unicodeID] = func

    def DeleteScreen(self):
        self.root.Screens.discard(self)

    def OnFrame(self, _id, func):
        self.OnF[_id] = func

    def render(self, event=None):
        if event:
            if event.type == pygame.QUIT:
                self.root.Running = False

            elif event.type == pygame.KEYUP:
                unicodeID = event.key
                for code in self.press:
                    if unicodeID == code:
                        self.press[code](self, event)

            for item in self.EventAble:
                item.update(event)
        else:
            for fr in self.OnF:
                self.OnF[fr]()

            for item in self.Items:
                item.update()

            for item in self.EventAble:
                item.update()
