class GameStats():
    '''跟踪游戏的统计信息'''

    def __init__(self, ai_settings):
        self.ai_settings = ai_settings
        self.reset_stats()
        #添加一个游戏状态的标识位
        self.game_active = True


    def reset_stats(self):
        '''初始化在邮箱运行期间可能变化的统计信息'''
        self.ships_left = self.ai_settings.ship_limit