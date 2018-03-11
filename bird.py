import random

# list of all possible players (tuple of 3 positions of flap)
BIRDS_LIST = (
    # red bird
    (
        'assets/sprites/redbird-upflap.png',
        'assets/sprites/redbird-midflap.png',
        'assets/sprites/redbird-downflap.png',
    ),
    # blue bird
    (
        # amount by which base can maximum shift to left
        'assets/sprites/bluebird-upflap.png',
        'assets/sprites/bluebird-midflap.png',
        'assets/sprites/bluebird-downflap.png',
    ),
    # yellow bird
    (
        'assets/sprites/yellowbird-upflap.png',
        'assets/sprites/yellowbird-midflap.png',
        'assets/sprites/yellowbird-downflap.png',
    ),
)


class Bird:
    def __init__(self):
        global BIRDS_LIST
        bird_index = random.randint(0, len(BIRDS_LIST) - 1)
        self.bird_name_list = list(BIRDS_LIST[bird_index])
