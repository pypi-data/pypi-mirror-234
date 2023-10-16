import pygame

from .base import itemBase
from ..Items.Screen import Screen


class Ellipse(itemBase):
    def __init__(self, screen: Screen, xy=(0, 0), wh=(50, 50), color="white", width=0):
        self.rect = pygame.Rect((0, 0), (0, 0))

        self.screen = screen
        screen.Items.append(self)

        self.xy = xy
        self.wh = wh
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(xy, wh)

    def config(self, xy, wh, color, width):
        self.xy = xy
        self.wh = wh
        self.color = color
        self.width = width
        self.rectE = pygame.Rect(xy, wh)

    def update(self):
        self.rect = pygame.draw.ellipse(self.screen.root.MainRoot, self.color, self.rectE, self.width)
