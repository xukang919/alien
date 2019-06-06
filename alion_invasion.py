
from settings import setting
from ship import Ship
from game_status import GameStatus
from scoreboard import ScoreBoard
from button import Button
import game_functions as gf

from pygame.sprite import Group

import pygame



ai_settings = setting()


def run_game():
    pygame.init()
    screen = pygame.display.set_mode((ai_settings.screen_width, ai_settings.screen_height))
    pygame.display.set_caption('Alion Tnvasion')

    play_button = Button(screen, 'Play')
    status = GameStatus(ai_settings)
    sb = ScoreBoard(ai_settings, screen, status)
    ship = Ship(ai_settings, screen)
    bullets = Group()
    aliens = Group()
    gf.create_fleet(ai_settings, screen, ship, aliens)


    while True:
        gf.check_events(ai_settings, screen, status, ship, aliens, bullets, play_button, sb)

        if  status.game_active == True:
            ship.update()
            gf.update_bullets(ai_settings, screen, status,ship, aliens, bullets, sb)
            gf.update_aliens(ai_settings, screen, status, ship, aliens, bullets, sb)

        gf.update_screen(ai_settings, screen, status, ship,  aliens, bullets, play_button, sb)


run_game()