class Settings:
    def __init__(self):
        #screensetting
        self.screen_width=1000
        self.screen_height=800
        self.bgcolor=(255,255,255)
        self.ship_speed=1.5
        self.bullet_speed = 3
        self.bullet_width =71
        self.bullet_height =15
        self.bullet_color =(60,60,60)
        self.bullet_allowed=100
        self.alien_speed =1.0
        self.fleet_direction = 1
        #self.fleet_drop=1
        self.fleet_drop_speed=10
        self.ship_limit=3