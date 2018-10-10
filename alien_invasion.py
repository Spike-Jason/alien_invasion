import sys

import pygame
from pygame.sprite import Group

from setting import Settings
from ship import Ship
import game_functions as gf
# from alien import Alien
from game_stats import GameStats


def run_game():
    #初始化游戏并创建一个屏幕对象
    pygame.init()
    ai_setting = Settings()
    screen = pygame.display.set_mode((ai_setting.screen_width, ai_setting.screen_height))
    pygame.display.set_caption('Alien Invasion')

    stats = GameStats(ai_setting)

    #设置背景颜色
    bg_color = (ai_setting.bg_color)

    #创建一个飞船
    ship = Ship(ai_setting, screen)

    #创建一个存储子弹的编组
    bullets = Group()

    #创建一个外星人
    # alien = Alien(ai_setting, screen)
    #创建一个外星人编组
    aliens = Group()

    gf.create_fleet(ai_setting, screen, ship, aliens)

    while True:


        gf.check_events(ai_setting, screen, ship, bullets)

        if stats.game_active:
            ship.update()
            gf.update_bullets(ai_setting, screen, ship, aliens, bullets)
            gf.update_aliens(ai_setting, stats, screen, ship, aliens, bullets)
        gf.update_screen(ai_setting, screen, ship, aliens, bullets)


if __name__ == '__main__':
    run_game()