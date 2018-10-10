import pygame
from pygame.sprite import Sprite

class Bullet(Sprite):
    '''一个对飞船发射的子弹进行管理的类'''

    def __init__(self, ai_settings, screen, ship):
        # super(Bullet, self).__init__()
        super().__init__()
        self.screen = screen

        #在原点创建子弹的矩形，然后在设置正确的位置
        self.rect = pygame.Rect(0, 0, ai_settings.bullet_width, ai_settings.bullet_height)
        self.rect.centerx = ship.rect.centerx
        self.rect.top = ship.rect.top

        #存储用小数表示子弹位置
        self.y = float(self.rect.y)

        self.color = ai_settings.bullet_color
        self.speed_factor = ai_settings.bullet_speed_factor

    def update(self, *args):
        '''向上移动子弹'''
        self.y -= self.speed_factor
        #更新子弹的位置
        self.rect.y = self.y

    def draw_bullet(self):
        pygame.draw.rect(self.screen, self.color, self.rect)