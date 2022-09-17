# stores all the settings in Alien Invasion
class Settings():

    def __init__(self):

        self.screen_width = 1200
        self.screen_height = 800
        self.bg_color = (200,150,200)

        self.ship_limit = 3

    #Bullet settings
        self.bullet_width = 3
        self.bullet_height = 15
        self.bullet_color = 60,60,60
        self.bullets_allowed = 10 

        self.fleet_drop_speed = 10

        self.speed_up_scale = 1.1

        self.alien_points = 50
        self.score_scale = 1.5

        self.initialize_dynamic_settings() #to initialize values for attributes that need to change during the game

    def initialize_dynamic_settings(self): # basically the default values for what does change later
        self.ship_speed_factor = 1.5
        self.bullet_speed_factor = 3
        self.alien_speed_factor = 1

        self.fleet_direction = 1 # move to the right

    def increase_speed(self):
        self.ship_speed_factor *= self.speed_up_scale
        self.bullet_speed_factor *= self.speed_up_scale
        self.alien_speed_factor *= self.speed_up_scale
        self.alien_points *= self.score_scale
