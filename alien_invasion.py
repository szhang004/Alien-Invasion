import sys
import pygame
from pygame.sprite import Group
from settings import Settings
from ship import Ship
from alien import Alien
import game_functions as gf
from game_stats import GameStats
from button import Button
from scoreboard import Scoreboard

def run_game():

# Create game & screen
    pygame.init()
    ai_settings = Settings()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption("Alien Invasion")

    stats = GameStats(ai_settings)
    play_button = Button(ai_settings, screen, "Play")
    sb = Scoreboard(ai_settings, screen, stats)

    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()

    gf.create_fleet(ai_settings, screen, aliens)

# Start game
    while True:

    # Check events
        gf.check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens)
        gf.update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb)

        if stats.game_active:
            ship.update()    
            gf.update_bullets(bullets, aliens, ai_settings, stats, sb)
            gf.update_aliens(ai_settings, stats, screen, aliens, ship, bullets, sb)
 

run_game()