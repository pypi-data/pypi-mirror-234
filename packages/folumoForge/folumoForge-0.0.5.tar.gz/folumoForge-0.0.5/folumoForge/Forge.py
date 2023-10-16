from os import environ

from pygame import Surface
from pygame.event import Event

from .Items.Screen import Screen

if "PYGAME_HIDE_SUPPORT_PROMPT" in environ:
    import pygame
else:
    environ["PYGAME_HIDE_SUPPORT_PROMPT"] = "1"
    import pygame

del environ


class Forge:
    def __init__(self, title, wh, icon=None, defaultScreen="start", fullScreen=False):
        pygame.init()
        pygame.font.init()

        self.Screens = {}
        self.Running = True
        self.modThreads = {}

        self.NewEventList: list[Event] = []
        self.InEvent = False

        self.delta_time = 0

        self.wh = wh
        self.MainRoot = Surface((0, 0))
        self.clock = pygame.time.Clock()
        pygame.display.set_caption(title)

        self.Screens[defaultScreen] = Screen(self, defaultScreen, wh, title, fullScreen)

        self.Screen = defaultScreen

        self.Screens[self.Screen].SwitchScreen()

        if icon:
            pygame.display.set_icon(pygame.image.load(icon))

    def GetScreen(self, name):
        return self.Screens.get(name)

    def NewScreen(self, screen):
        self.Screens[screen.name] = screen

    def Run(self):
        while True:
            try:
                self._run()
                break
            except RuntimeError:
                pass

    def _run(self):
        while self.Running:
            self.delta_time = self.clock.tick(60)
            self.MainRoot.fill((0, 0, 0))
            self.Screens[self.Screen].render()

            for event in pygame.event.get():
                self.Screens[self.Screen].render(event)

            pygame.display.update()

        pygame.quit()
        pygame.font.quit()
