from constants import *
from constants import _base10_to_base2
from block import Block


class Encoder:
    def __init__(self):
        self.reset()

    def reset(self):
        self.blocks = [Block() for _ in range(BLOCK_COUNT)]
        self.message_length = 0

    def encode_message(self, message):
        if len(message) > MAX_MESSAGE_SIZE:
            raise Exception("message is too long")
        self.message_length = len(message)
        # encode
        for i, char in enumerate(message):
            block = self.blocks[i // BLOCK_CHAR_SIZE]
            index = i % BLOCK_CHAR_SIZE
            block.write_data(index, char)
        # fill unused
        for i in range(self.message_length, MAX_MESSAGE_SIZE):
            block = self.blocks[i // BLOCK_CHAR_SIZE]
            index = i % BLOCK_CHAR_SIZE
            block.write_data(index, chr(BLANK_CHAR_CODE))
        # ecc
        for block in self.blocks:
            block.write_error_correct()
        # mask
        for block in self.blocks:
            block.write_mask()
        # metadata
        self.write_meta_data()

    def write_meta_data(self):
        block = self.blocks[BLOCK_COUNT - 1]
        # 12 groups total
        # sample group - 6
        block.write_sample_group(GROUP_HEIGHT, 0)
        # message length - 1
        block.write_group(GROUP_HEIGHT * 2, GROUP_WIDTH * 3,
                          _base10_to_base2(self.message_length))
        # version - 1
        block.write_group(GROUP_HEIGHT * 2, GROUP_WIDTH *
                          4, _base10_to_base2(VERSION))
        # mask - 1
        block.write_group(GROUP_HEIGHT * 2, GROUP_WIDTH * 5,
                          _base10_to_base2(MASK_TYPE))
        # unused - 3
        for i in range(3, 6):
            block.write_group(GROUP_HEIGHT, GROUP_WIDTH * i,
                              _base10_to_base2(255))
