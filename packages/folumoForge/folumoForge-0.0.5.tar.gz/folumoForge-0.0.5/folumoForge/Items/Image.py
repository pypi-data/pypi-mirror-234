import pygame

from .base import itemBase
from ..Items import Screen


class Image(itemBase):
    def __init__(self, screen: Screen, path, xy, wh=None):
        self.screen = screen
        screen.Items.append(self)
        self.xy = xy

        self.img = pygame.image.load(path)
        if wh:
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def config(self, path, xy, wh=None):
        self.xy = xy

        self.img = pygame.image.load(path)
        if wh:
            self.img = pygame.transform.scale(self.img, wh)

        self.rect = self.img.get_rect()

    def update(self):
        self.screen.root.MainRoot.blit(self.img, self.xy)