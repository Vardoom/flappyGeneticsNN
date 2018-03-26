def load_parameters():
    with open("parameters.txt", "r") as file:
        parameters = file.readlines()
        # print(parameters)
    p = list()
    for param in parameters:
        if '=' in param and "True" not in param and "False" not in param:
            # print(param)
            index_beg = param.find('=')
            index_end = param.find("\n")
            p.append(float(param[index_beg + 2: index_end]))
        elif '=' in param:
            index_beg = param.find('=')
            index_end = param.find("\n")
            s = param[index_beg + 2: index_end]
            # print(s)
            if s == "True":
                p.append(True)
            else:
                p.append(False)
    return p


parameters = load_parameters()
# print(parameters)

FPS = 30
SCREEN_WIDTH = 288.0
SCREEN_HEIGHT = 512.0
PIPE_GAP_SIZE = 100
BASE_Y = SCREEN_HEIGHT * 0.79

PIPE_VEL_X = -4
BIRD_MAX_VEL_Y = 10
BIRD_MIN_VEL_Y = -8
BIRD_FLAP_ACC = -9

N_GENERATION = int(parameters[0])
print("N_GENERATION = {}".format(N_GENERATION))
N_POPULATION = int(parameters[1])
print("N_POPULATION = {}".format(N_POPULATION))
MAX_SCORE = int(parameters[2])
print("MAX_SCORE = {}".format(MAX_SCORE))
MUTATION_THRESHOLD = parameters[3]
print("MUTATION_THRESHOLD = {}".format(MUTATION_THRESHOLD))

LOAD_POP = parameters[4]
print("LOAD_POP = {}".format(LOAD_POP))
SAVE_POP = parameters[5]
print("SAVE_POP = {}".format(SAVE_POP))
