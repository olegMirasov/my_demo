NUMBERS = [str(i) for i in range(0, 5)]
COINS = [1, 5, 10]

# casino commands
COM_EXIT = '/exit'
COM_COIN = '/coin'  # + coin value
RED = 'red'
BLACK = 'black'
GREEN = 'green'
# NUMBERS так же считаются как команды

COLOR_DICT = {
    NUMBERS[0]: GREEN
}

flag = True
for i in range(1, len(NUMBERS)):
    color = [RED, BLACK][flag]
    flag = not flag
    COLOR_DICT[NUMBERS[i]] = color
