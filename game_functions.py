import sys
from time import sleep

import pygame


from alien import Alien
from bullet import Bullet

def check_keydown_events(event, ai_settings, screen, ship, bullets):
    '''响应按键'''
    if event.key == pygame.K_RIGHT:
        # ship.rect.centerx += 1
        ship.moving_right = True
    if event.key == pygame.K_LEFT:
        ship.moving_left = True
    if event.key == pygame.K_SPACE:
        fire_bullet(ai_settings, screen, ship, bullets)
    if event.key == pygame.K_q:
        sys.exit()

def fire_bullet(ai_settings, screen, ship, bullets):
    '''如果还没有到达子弹限制，就发一个子弹'''
    if len(bullets) < ai_settings.bullets_allowed:
        new_bullet = Bullet(ai_settings, screen, ship)
        bullets.add(new_bullet)

def check_keyup_events(event, ship):
    if event.key == pygame.K_RIGHT:
        ship.moving_right = False
    if event.key == pygame.K_LEFT:
        ship.moving_left = False


def check_events(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets):
    '''响应键盘和鼠标事件'''
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            sys.exit()

        elif event.type == pygame.KEYDOWN:
            check_keydown_events(event, ai_settings, screen, ship, bullets)

        elif event.type == pygame.KEYUP:
            check_keyup_events(event, ship)

        elif event.type == pygame.MOUSEBUTTONDOWN:
            mouse_x, mouse_y = pygame.mouse.get_pos()
            check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y)


def check_play_button(ai_settings, screen, stats, sb, play_button, ship, aliens, bullets, mouse_x, mouse_y):
    '''玩家单击鼠标开始游戏'''
    #判断鼠标是否点击到按钮
    button_clicked = play_button.rect.collidepoint(mouse_x, mouse_y)
    #当按钮被点击，且游戏状态为False 才开始（初始状态为False, not stats.game_active 为True 所以下面判断成立）。
    if button_clicked and not stats.game_active:

        #重置游戏速度
        ai_settings.initialize_dynamic_setting()
        #隐藏鼠标
        pygame.mouse.set_visible(False)

        #重置游戏统计数据
        stats.reset_stats()
        stats.game_active = True

        #重置记分牌图像
        sb.prep_score()
        sb.prep_high_score()
        sb.prep_level()
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建新的一群外星人，并设置飞船
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

def create_fleet(ai_settings, screen, ship, aliens):
    '''创建外星人群'''
    #创建一个外星人，并计算每一行可容纳的个数
    alien = Alien(ai_settings, screen)
    number_aliens_x = get_number_aliens_x(ai_settings, alien.rect.width)
    number_rows = get_number_rows(ai_settings, ship.rect.height, alien.rect.height)

    #创建外星人群
    # for alien_number in range(number_aliens_x):
    #     create_alien(ai_settings, screen, aliens, alien_number)
    for row_number in range(number_rows):
        for alien_number in range(number_aliens_x):
            create_alien(ai_settings, screen, aliens, alien_number, row_number)

def get_number_aliens_x(ai_settings, alien_width):
    available_space_x = ai_settings.screen_width - 2 * alien_width
    number_aliens_x = int(available_space_x / (2 * alien_width))
    return number_aliens_x

def create_alien(ai_settings, screen, aliens, alien_number, row_number):
    alien = Alien(ai_settings, screen)
    alien_width = alien.rect.width
    alien.x = alien_width + 2 * alien_width * alien_number
    alien.rect.x = alien.x
    alien.rect.y = alien.rect.height + 2 * alien.rect.height * row_number
    aliens.add(alien)

def get_number_rows(ai_settings, ship_height, alien_height):
    '''计算屏幕可容纳多少行外星人'''
    available_space_y = (ai_settings.screen_height - (3 * alien_height) - ship_height)
    number_rows = int(available_space_y / (2 * alien_height))
    return number_rows

def update_screen(ai_settings, screen, stats, sb, ship, aliens, bullets, play_button):
    # 每次循环重新绘制屏幕
    screen.fill(ai_settings.bg_color)
    for bullet in bullets.sprites():
        bullet.draw_bullet()
    ship.blitme()
    # aliens.blitme()
    aliens.draw(screen)
    sb.show_score()

    #如果游戏处于非活动状态，就绘制Play按钮
    if not stats.game_active:
        play_button.draw_button()
    # 让最近绘制的屏幕可见
    pygame.display.flip()

def update_bullets(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''更新子弹的位置，并删除已经消失的子弹'''
    #更新位置
    bullets.update()

    #删除子弹
    for bullet in bullets.copy():
        if bullet.rect.bottom <= 0:
            bullets.remove(bullet)
    check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_bullet_alien_collisions(ai_settings, screen, stats, sb, ship, aliens, bullets):
    #检查是否有子弹击中外星人
    collisions = pygame.sprite.groupcollide(bullets, aliens, True, True)

    #计分更新,如果碰撞发送，循环确认碰撞的次数，
    if collisions:
        for aliens in collisions.values():
            stats.score += ai_settings.alien_points * len(aliens)
            sb.prep_score()
        check_high_score(stats, sb)
    if len(aliens) == 0:
        #删除现有的子弹并新建一群外星人
        bullets.empty()
        #加快游戏节奏
        ai_settings.increase_speed()
        create_fleet(ai_settings, screen, ship, aliens)

        #提高等级
        stats.level += 1
        sb.prep_level()

def check_fleet_edges(ai_settings, aliens):
    '''有外星人滴答边缘时采取措施'''
    for alien in aliens.sprites():
        if alien.check_edges():
            change_fleet_direction(ai_settings, aliens)
            break

def change_fleet_direction(ai_settings, aliens):
    '''将整群下移并改变方向'''
    for alien in aliens.sprites():
        alien.rect.y += ai_settings.fleet_drop_speed
    ai_settings.fleet_direction *= -1



def ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets):
    '''响应被外星人撞到飞船'''
    if stats.ships_left > 0:
        stats.ships_left -= 1

        #更新计分牌
        sb.prep_ships()

        #清空外星人列表和子弹列表
        aliens.empty()
        bullets.empty()

        #创建一群新的外星人,并将飞船放在初始位置
        create_fleet(ai_settings, screen, ship, aliens)
        ship.center_ship()

        sleep(0.5)

    else:
        stats.game_active = False
        #创新显示鼠标
        pygame.mouse.set_visible(True)


def check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''检查是否有外星人到达底部'''
    screen_rect = screen.get_rect()
    for alien in aliens.sprites():
        if alien.rect.bottom >= screen_rect.bottom:
            ship_hit(ai_settings, stats, screen, ship, aliens,bullets)
            break

def update_aliens(ai_settings, screen, stats, sb, ship, aliens, bullets):
    '''检查是否有外星人处于屏幕边缘，并更新整群外星人位置'''
    check_fleet_edges(ai_settings, aliens)
    aliens.update()

    #检查外星人和飞船相撞
    if pygame.sprite.spritecollideany(ship, aliens):
        # print("Ship hit!!")
        ship_hit(ai_settings, stats, screen, sb, ship, aliens, bullets)
    #检查外星人是否到达底部
    check_aliens_bottom(ai_settings, screen, stats, sb, ship, aliens, bullets)

def check_high_score(stats, sb):
    '''检查是否有新的最高分'''
    if stats.score > stats.high_score:
        stats.high_score = stats.score
        sb.prep_high_score()