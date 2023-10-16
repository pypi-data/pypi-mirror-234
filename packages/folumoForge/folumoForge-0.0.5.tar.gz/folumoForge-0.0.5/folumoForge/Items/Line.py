import pygame.draw

from .base import itemBase
from ..Items.Screen import Screen


class Line(itemBase):
    def __init__(self, screen: Screen, a=(0, 0), b=(10, 10), width=1, color="white"):
        self.rect = pygame.Rect((0, 0), (0, 0))
        self.screen = screen
        screen.Items.append(self)
        self.a = a
        self.b = b
        self.width = width
        self.color = color

    def config(self, a=(0, 0), b=(10, 10), width=1, color="white"):
        self.a = a
        self.b = b
        self.width = width
        self.color = color
        
    def update(self):
        self.rect = pygame.draw.line(self.screen.root.MainRoot, self.color, self.a, self.b, self.width)
