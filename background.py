import random

# list of backgrounds
BACKGROUNDS_LIST = ['assets/sprites/background-day.png', 'assets/sprites/background-night.png']


class Background:
    def __init__(self):
        global BACKGROUNDS_LIST
        rand_bg = random.randint(0, len(BACKGROUNDS_LIST) - 1)
        self.background_name = BACKGROUNDS_LIST[rand_bg]
