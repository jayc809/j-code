from constants import *
from constants import _base10_to_base2, _base2_to_base_10
import itertools


class Block:
    def __init__(self):
        self.data = [[0 for _ in range(BLOCK_BIT_SIZE)]
                     for _ in range(BLOCK_BIT_SIZE)]

    def write_bit(self, row, col, val):
        self.data[row][col] = val

    def write_data(self, index, char):
        rows, cols = self._get_rows(index), self._get_cols(index)
        encoding = _base10_to_base2(ord(char))
        i = 0
        for row, col in itertools.product(rows, cols):
            self.data[row][col] = encoding[i]
            i += 1

    def read_data(self, index):
        rows, cols = self._get_rows(index), self._get_cols(index)
        bits = []
        for row, col in itertools.product(rows, cols):
            bits.append(self.data[row][col])
        ascii_code = _base2_to_base_10(bits)
        return chr(ascii_code)

    def write_error_correct(self):
        for row in range(BLOCK_BIT_SIZE):
            for start_col, step_size in ERROR_CORRECTION_PAIRS:
                group = [sum(self.data[row][col: col + step_size])
                         for col in range(start_col, BLOCK_BIT_SIZE, step_size * 2)]
                parity = sum(group) % 2
                if parity == 1:
                    self.data[row][start_col] = 1
                else:
                    self.data[row][start_col] = 0

    def error_correct(self, block_id, is_metadata=False):
        for row in range(BLOCK_BIT_SIZE):
            if is_metadata and row == GROUP_HEIGHT:
                return
            errors = []
            for start_col, step_size in ERROR_CORRECTION_PAIRS:
                group = [sum(self.data[row][col: col + step_size])
                         for col in range(start_col, BLOCK_BIT_SIZE, step_size * 2)]
                parity = sum(group) % 2
                if parity == 1:
                    errors.append(step_size)
            if len(errors) == 0:
                continue
            error_bit = sum(errors) - 1
            print(f"error detected in block{block_id} at ({row},{error_bit})")
            self.data[row][error_bit] = (self.data[row][error_bit] + 1) % 2

    def write_mask(self):
        for row in range(BLOCK_BIT_SIZE):
            for col in range(BLOCK_BIT_SIZE):
                if (row + col) % 3 == 0:
                    self.data[row][col] = (self.data[row][col] + 1) % 2

    def write_group(self, start_row, start_col, encoding):
        i = 0
        for row, col in itertools.product(range(start_row, start_row + GROUP_HEIGHT), range(start_col, start_col + GROUP_WIDTH)):
            self.data[row][col] = encoding[i]
            i += 1

    def read_group(self, start_row, start_col):
        bits = []
        for row, col in itertools.product(range(start_row, start_row + GROUP_HEIGHT), range(start_col, start_col + GROUP_WIDTH)):
            bits.append(self.data[row][col])
        return _base2_to_base_10(bits)

    def write_sample_group(self, start_row, start_col):
        for d_row in range(GROUP_HEIGHT // 2):
            for d_col in range(GROUP_WIDTH * 3):
                self.data[start_row + d_row][start_col + d_col] = 1
        for d_row in range(GROUP_HEIGHT // 2, (GROUP_HEIGHT // 2) + GROUP_HEIGHT):
            for d_col in range(GROUP_WIDTH * 3):
                color = 1 if d_col // GROUP_WIDTH != 1 else 0
                self.data[start_row + d_row][start_col + d_col] = color
        for d_row in range((GROUP_HEIGHT // 2) + GROUP_HEIGHT, GROUP_HEIGHT * 2):
            for d_col in range(GROUP_WIDTH * 3):
                self.data[start_row + d_row][start_col + d_col] = 1

    def _get_rows(self, index):
        group_row = index // BLOCK_NUM_COLS
        block_rows = GROUP_ROW_TO_BLOCK_ROWS[group_row]
        return block_rows

    def _get_cols(self, index):
        group_col = index % BLOCK_NUM_COLS
        block_cols = GROUP_COL_TO_BLOCK_COLS[group_col]
        return block_cols
