import sys
import pygame

from bullet import Bullet
from alien import Alien
from time import sleep
from button import Button

def check_events(ai_settings, screen, ship, bullets, stats, play_button, aliens):
    # Watching events
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)
        
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, bullets, ship) 
        

def update_screen(ai_settings, screen, ship, aliens, bullets, stats, play_button, sb):
    screen.fill(ai_settings.bg_color) 
    sb.show_score()

    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen) # automatically draws every element of the group

    if not stats.game_active:
        play_button.draw_button()

    # Makes most recent screen visible
    pygame.display.flip()

def check_keydown_events(event,ai_settings, screen,ship,bullets):
    if event.key == pygame.K_RIGHT: # move ship to right
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullets(ai_settings, screen, ship, bullets)
    elif event.key == pygame.K_q:
        sys.exit()

def check_keyup_events(event,ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False

def fire_bullets(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def update_bullets(bullets, aliens, ai_settings, stats, sb):
    bullets.update()

    for bullet in bullets.copy(): # must use copy() to modify inside
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    print(len(bullets))

    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)  # True values mean both disappear after collision
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens) # ensures 2 aliens hit in same loop doesn't get missed out
            sb.prep_score()
        check_high_score(stats, sb)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width # fill up whole width - margins of 1 alien
    number_aliens_x = int(available_space_x / (2*alien_width))
    return number_aliens_x

def get_number_rows(ai_settings, alien_height):
    number_aliens_y = int((ai_settings.screen_height - 3 * alien_height) / (2 * alien_height))
    return number_aliens_y

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.y = alien_height + 2 * alien_height * row_number
    alien.rect.y = alien.y
    aliens.add(alien)

def create_fleet(ai_settings, screen, aliens):
# calculate how many fit in one row
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien_height = alien.rect.height
    number_aliens_x = get_number_aliens_x(ai_settings, alien_width)
    number_aliens_y = get_number_rows(ai_settings, alien_height)
    
    for row_number in range(number_aliens_y):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def update_aliens(ai_settings, stats, screen, aliens, ship, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens): # looks for collisions between sprite and any member of group
        ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
        
    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed() # level up basically
        create_fleet(ai_settings, screen, aliens)
        stats.level += 1 
        sb.prep_level()

def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed # drop it one level and switch directions
    ai_settings.fleet_direction *= -1 

def ship_hit(ai_settings, stats, screen, ship, aliens, bullets):
    if ships_left > 0: 
        stats.ships_left -= 1 
        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()

        sleep(0.5)
    else:
        stats.game_active = False

def check_aliens_bottom(ai_settings, stats, screen, ship, aliens, bullets):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens, bullets)
            break

def check_play_button(stats, play_button, mouse_x, mouse_y, ai_settings, screen, aliens, bullets, ship):
    if play_button.rect.collidepoint(mouse_x, mouse_y) and not stats.game_active: # to make sure you can't click after button disappears
        stats.game_active = True
    
        stats.reset_stats()

        ai_settings.initialize_dynamic_settings()

        aliens.empty()
        bullets.empty()

        create_fleet(ai_settings, screen, aliens)
        ship.center_ship()
        pygame.mouse.set_visible(False)

def check_high_score(stats, sb):
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()   # resets high score