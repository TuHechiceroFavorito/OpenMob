from mock_up import *


# Looping 10 times to see how the system behaves
for i in list(range(10)):
    print("------------------------------------")
    # Call all different modules
    b = bluetooth()
    u = ultrasound()
    o = object()
    p = path()
    m = maps()

    # Print output from the modules
    print(b, u, o, p, m)

    # Give an initial value to action
    action = None


    # What if one of the inputs is Null


    # Implement look-up table
    # s - Stop
    # F - Free
    # R - Right
    # L - Left

    if b == None or u == None or o == None or p == None or m == None:
        action = "Stop"

    elif b == "S" or u == "S":
        action = "Stop"

    elif o != "F":
        action = o

    elif p != "F":
        action = p

    elif m != "F":
        action = m

    else:
        action = "F"

    print(action)

    print("------------------------------------")