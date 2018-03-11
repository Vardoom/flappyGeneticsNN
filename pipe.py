import random as rd

# list of pipes
PIPES_LIST = (
    'assets/sprites/pipe-green.png',
    'assets/sprites/pipe-red.png',
)


class Pipe:

    def __init__(self):
        global PIPES_LIST
        pipe_index = rd.randint(0, len(PIPES_LIST) - 1)
        self.pipe_name = PIPES_LIST[pipe_index]
