class Settings():
    '''存储游戏的所有设置类'''

    def __init__(self):
        '''初始化游戏的设置'''
        #屏幕设置
        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (230, 230, 230)

        #飞船的设置
        self.ship_speed_factor = 30
        self.ship_limit = 3

        #子弹的设置
        self.bullet_speed_factor = 15.5
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60, 60, 60
        self.bullets_allowed = 3

        #外星人设置
        self.alien_speed_factor = 30
        self.fleet_drop_speed = 10
        #设置一个标识位 1为右 -1 为左
        self.fleet_direction = 1

        #设置游戏提升速度
        self.speedup_scale = 1.1
        self.initialize_dynamic_setting()
        self.score_scale = 1.5

        #计分
        self.alien_points = 50

    def initialize_dynamic_setting(self):
        '''初始化随游戏进行而变化设置'''
        self.ship_speed_factor = 30
        self.bullet_speed_factor = 15.5
        self.alien_speed_factor = 30

        self.fleet_direction = 1

    def increase_speed(self):
        '''提高速度设置和外星人点数'''
        self.ship_speed_factor *= self.speedup_scale
        self.bullet_speed_factor *= self.speedup_scale
        self.alien_speed_factor *= self.speedup_scale

        self.alien_points = int(self.alien_points * self.score_scale)