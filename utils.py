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
        if '=' in param and ("True" in param or "False" in param):
            # print(param)
            index_beg = param.find('=')
            index_end = param.find("\n")
            s = param[index_beg + 2: index_end]
            if s == "True":
                p.append(True)
            else:
                p.append(False)
    return p


parameters = load_parameters()

FPS = parameters[0]
print("FPS = {}".format(FPS))
SCREEN_WIDTH = parameters[1]
print("SCREEN_WIDTH = {}".format(SCREEN_WIDTH))
SCREEN_HEIGHT = parameters[2]
print("SCREEN_HEIGHT = {}".format(SCREEN_HEIGHT))  # amount by which base can maximum shift to left
PIPE_GAP_SIZE = parameters[3]  # gap between upper and lower part of pipe
print("PIPE_GAP_SIZE = {}".format(PIPE_GAP_SIZE))
BASE_Y = SCREEN_HEIGHT * 0.79
print("BASE_Y = {}".format(BASE_Y))

PIPE_VEL_X = parameters[4]
print("PIPE_VEL_X = {}".format(PIPE_VEL_X))
BIRD_MAX_VEL_Y = parameters[5]  # max vel along Y, max descend speed
print("BIRD_MAX_VEL_Y = {}".format(BIRD_MAX_VEL_Y))
BIRD_MIN_VEL_Y = parameters[6]  # min vel along Y, max ascend speed
print("BIRD_MIN_VEL_Y = {}".format(BIRD_MIN_VEL_Y))
BIRD_FLAP_ACC = parameters[7]  # players speed on flapping
print("BIRD_FLAP_ACC = {}".format(BIRD_FLAP_ACC))

N_GENERATION = int(parameters[8])
print("N_GENERATION = {}".format(N_GENERATION))
N_POPULATION = int(parameters[9])
print("N_POPULATION = {}".format(N_POPULATION))
MAX_SCORE = int(parameters[10])
print("MAX_SCORE = {}".format(MAX_SCORE))

THRESHOLD = parameters[11]
print("THRESHOLD = {}".format(THRESHOLD))
LOAD_POP = parameters[12]
print("LOAD_POP = {}".format(LOAD_POP))
SAVE_POP = parameters[13]
print("SAVE_POP = {}".format(SAVE_POP))
