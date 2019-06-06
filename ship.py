import pygame
from pygame.sprite import Sprite

class Ship(Sprite):

    def __init__(self, ai_settings, screen):

        super().__init__()

        self.screen = screen
        self.ai_settings = ai_settings

        self.screen_rect = screen.get_rect()
        self.image = pygame.image.load('./images/ship.bmp')
        self.rect  = self.image.get_rect()

        self.rect.centerx = self.screen_rect.centerx
        self.rect.bottom = self.screen_rect.bottom


        self.moving_right = False
        self.moving_left = False

        self.centerx = float(self.rect.centerx)

    def update(self):

        if self.moving_right == True and self.rect.right < self.screen_rect.right:
            self.centerx += self.ai_settings.ship_speed

        if self.moving_left == True and self.rect.left > self.screen_rect.left:
            self.centerx -= self.ai_settings.ship_speed

        self.rect.centerx = self.centerx

    def blitme(self):
        self.screen.blit(self.image, self.rect)

    def center_ship(self):
        self.centerx = self.screen_rect.centerx

