from PIL import Image
from pprint import pprint
from constants import *
from block import Block


class Decoder:
    def __init__(self):
        self.code_path = None
        self.message = ""

    def translate_code(self):
        message = ""
        try:
            bit_data = self.get_bit_data_from_image()
            blocks = self.get_blocks_from_bit_data(bit_data)
            self.blocks = blocks
            message_length = self.get_message_length()
            for i, block in enumerate(blocks):
                block.write_mask()
                block.error_correct(
                    block_id=i, is_metadata=(i == BLOCK_COUNT - 1))
            for i in range(message_length):
                block_i = i // BLOCK_CHAR_SIZE
                block = self.blocks[block_i]
                index = i % BLOCK_CHAR_SIZE
                char = block.read_data(index)
                message += char
            self.message = message
        except Exception as e:
            print(e)
        return message

    def get_message_length(self):
        block = self.blocks[-1]
        return block.read_group(GROUP_HEIGHT * 2, GROUP_WIDTH * 3)

    def get_blocks_from_bit_data(self, bit_data):
        blocks = []
        for row, col in BLOCK_LOCATION.values():
            block = Block()
            start_row, start_col = row * BLOCK_BIT_SIZE, col * BLOCK_BIT_SIZE
            for block_row in range(BLOCK_BIT_SIZE):
                for block_col in range(BLOCK_BIT_SIZE):
                    grayscale_value = bit_data[start_row +
                                               block_row][start_col + block_col]
                    bit = 1 if grayscale_value < (255 / 2) else 0
                    block.write_bit(block_row, block_col, bit)
            blocks.append(block)
        return blocks

    def get_bit_data_from_image(self):
        if not self.code_path:
            raise Exception("no path found")
        with Image.open(self.code_path) as image:
            image.convert("L")
            image_scaled = image.resize(
                (BIT_COUNT, BIT_COUNT), resample=4)
            image_data = image_scaled.load()
        data_grayscale = []
        for row in range(BIT_COUNT):
            data_grayscale_row = []
            for col in range(BIT_COUNT):
                data_grayscale_row.append(
                    sum(image_data[col, row][:3]) / 3)
            data_grayscale.append(data_grayscale_row)
        return data_grayscale

    def add_code_path(self, path):
        self.code_path = path
