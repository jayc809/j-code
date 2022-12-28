import os

BLOCK_BIT_SIZE = 12
BLOCK_CHAR_SIZE = 12
BLOCK_NUM_ROWS = 3
BLOCK_NUM_COLS = 4
GROUP_NUM_BITS = 8
GROUP_WIDTH = 2
GROUP_HEIGHT = 4
MAX_MESSAGE_SIZE = 88
BLANK_CHAR_CODE = 128 + 64 + 8 + 4


def _base10_to_base2(base10):
    base2 = str(bin(base10))[2:]
    base2 = ("0" * (GROUP_NUM_BITS - len(base2))
             ) + base2
    return [int(bit) for bit in base2]


def _base2_to_base_10(base2):
    base2 = [str(bit) for bit in base2]
    base2 = "".join(base2)
    return int(base2, 2)


VERSION = 100
MASK_TYPE = 1

CODE_NUM_ROWS = 5
CODE_NUM_COLS = 5
BIT_COUNT = CODE_NUM_ROWS * BLOCK_BIT_SIZE
BLOCK_COUNT = 8
BLOCK_LOCATION = {
    0: (0, 3),
    1: (1, 3),
    2: (2, 3),
    3: (3, 3),
    4: (4, 3),
    5: (4, 2),
    6: (3, 1),
    7: (4, 1)
}

GROUP_ROW_TO_BLOCK_ROWS = {
    0: (0, 1, 2, 3),
    1: (4, 5, 6, 7),
    2: (8, 9, 10, 11)
}
GROUP_COL_TO_BLOCK_COLS = {
    0: (2, 4),
    1: (5, 6),
    2: (8, 9),
    3: (10, 11)
}
ERROR_CORRECTION_PAIRS = [(0, 1), (1, 2), (3, 4), (7, 8)]

WINDOW_WIDTH = 800
WINDOW_HEIGHT = 800
CODE_WIDTH = 540
CODE_HEIGHT = 540
PURPLE = "#9386FF"

CURRENT_DIR = os.path.dirname(os.path.abspath(__file__))
