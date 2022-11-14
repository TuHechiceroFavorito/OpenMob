import numpy as np

# All possible outputs from the different modules
OUTPUTS = ["R", "L", "F", None]
OUTPUTS_2 = ["S", "F"]

# Random functions to generate test outputs
def bluetooth():
    return OUTPUTS_2[np.random.randint(len(OUTPUTS_2))]

def object():
    return OUTPUTS[np.random.randint(len(OUTPUTS))]

def path():
    return OUTPUTS[np.random.randint(len(OUTPUTS))]

def ultrasound():
    return OUTPUTS_2[np.random.randint(len(OUTPUTS_2))]

def maps():
    return OUTPUTS[np.random.randint(len(OUTPUTS))]

if __name__ == "__main__":
    for i in list(range(10)):
        print("hey")