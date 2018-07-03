MAX_MASS = 50
MIN_MASS = 9
STEP = 5

def masses_generator():
    masses = []
    for mass1 in range(MAX_MASS, MIN_MASS, -STEP):
        for mass2 in range(mass1, MIN_MASS, -STEP):
            masses.append((mass1, mass2))

    return masses