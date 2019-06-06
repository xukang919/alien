import sys
from bullet import Bullet
from time import sleep
import pygame
from alien import Alien


def check_keydown_event(ai_settings, screen,  ship, bullets, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = True
    elif event.key == pygame.K_LEFT:
        ship.moving_left = True
    elif event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)


def check_keyup_event(ship, event):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    elif event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, status, ship, aliens, bullets, play_button, sb):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()
        elif event.type == pygame.KEYDOWN:
            check_keydown_event(ai_settings, screen, ship, bullets, event)
        elif event.type == pygame.KEYUP:
            check_keyup_event(ship, event)
        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, status, ship, aliens, bullets, play_button, sb, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, status, ship, aliens, bullets, play_button, sb, mouse_x, mouse_y):
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    if button_clicked and not status.game_active:
        ai_settings.initialize_dynamic_settings()
        pygame.mouse.set_visible(False)
        status.reset_status()
        status.game_active = True
        sb.prep_level()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()


def check_high_score(status, sb):
    if status.score > status.high_score:
        status.high_score = status.score
        sb.prep_high_score()


def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x


def get_number_rows(ai_settings, ship_height, alien_height):
    available_space_y = (ai_settings.screen_height - (3*alien_height) - ship_height)
    number_rows = int(available_space_y / (2*alien_height))
    return number_rows


def create_aliens(ai_settings, screen, alien_number, row_number, aliens):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2*alien_width*alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2*alien.rect.height*row_number
    aliens.add(alien)


def create_fleet(ai_settings, screen, ship, aliens):
    alien1 = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien1.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien1.rect.height)
    for number_row in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_aliens(ai_settings, screen, alien_number, number_row, aliens)


def change_fleet_direction(ai_settings, aliens):
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1


def check_fleet_edges(ai_settings, aliens):
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break


def ship_hit(ai_settings, screen, status, ship, aliens, bullets, sb):
    if status.ships_left > 0:
        status.ships_left -= 1
        sb.prep_ships()
        aliens.empty()
        bullets.empty()
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()
        sleep(0.5)
    else:
        status.game_active = False
        pygame.mouse.set_visible(True)


def check_alien_bottom(ai_settings, screen, status, ship, aliens, bullets, sb):
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, screen, status, ship, aliens, bullets, sb)
            break


def update_aliens(ai_settings, screen, status, ship, aliens, bullets, sb):
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    if pygame.sprite.spritecollideany(ship, aliens):
        ship_hit(ai_settings, screen,  status, ship, aliens, bullets, sb)

    check_alien_bottom(ai_settings, screen, status, ship, aliens, bullets, sb)


def fire_bullet(ai_settings, screen, ship, bullets):
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)


def check_bullet_alien_collisions(ai_settings, screen, status, ship, aliens, bullets, sb):
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    if collisions:
        for aliens in collisions.values():
            status.score += ai_settings.alien_points
            sb.prep_score()
        check_high_score(status, sb)

    if len(aliens) == 0:
        bullets.empty()
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        status.level += 1
        sb.prep_level()


def update_bullets(ai_settings, screen, status, ship, aliens, bullets, sb):
    bullets.update()
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, status, ship, aliens, bullets, sb)


def update_screen(ai_settings, screen, status, ship,  aliens, bullets, play_button, sb):
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    aliens.draw(screen)
    sb.show_score()
    if not status.game_active:
        play_button.draw_button()

    pygame.display.flip()
