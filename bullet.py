import pygame
from pygame.sprite import Sprite # to act on all the Bullets as one group of elements

class Bullet(Sprite):

    def __init__(self, ai_settings, screen, ship):
        super(Bullet, self).__init__()
        self.screen = screen
        self.rect = pygame.Rect(0,0,ai_settings.bullet_width,ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        self.y = float(self.rect.y) #store as a decimal

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self):

        self.y -= self.speed_factor  # to move up, minus y value lol
        self.rect.y = self.y # update rectangle position

    def draw_bullet(self):
        pygame.draw.rect(self.screen,self.color,self.rect)