import pygame

from ..Items import Screen
from ..Mods import modBase


class Text:
    def __init__(self, screen: Screen, font="Arial", text="Sample Text.", color="white", size=12, xy=(0, 0)):
        self.mods = {}
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.screen = screen
        screen.Items.append(self)

        self.xy = xy
        self.font = font
        self.text = text
        self.color = color
        self.size = size

        self.RenderedText = self._text()

    def _text(self):
        try:
            return pygame.font.Font(self.font, self.size).render(self.text, False, self.color)
        except FileNotFoundError:
            try:
                return pygame.font.SysFont(self.font, self.size, True).render(self.text, False, self.color)
            except ValueError:
                return pygame.font.SysFont("Ariel", 12, True).render("Sample Text", False, self.color)

    def config(self, font="Arial", text="Sample Text.", color="white", size=12, xy=(0, 0)):

        self.xy = xy
        self.font = font
        self.text = text
        self.color = color
        self.size = size

        self.RenderedText = self._text()

    def addMod(self, mod: modBase):
        if mod.name not in self.mods:
            self.mods[mod.name] = mod

    def update(self):
        self.rect = self.screen.root.MainRoot.blit(self.RenderedText, self.xy)
