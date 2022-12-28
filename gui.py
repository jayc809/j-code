import tkinter as tk
from tkinter import filedialog, font
from PIL import Image, ImageDraw
import os
from encoder import Encoder
from decoder import Decoder
from constants import *


class GUI:
    def __init__(self):
        root = tk.Tk()
        root.title("")
        root.geometry(f"{WINDOW_WIDTH}x{WINDOW_HEIGHT}")
        self.root = root

        # display
        display_frame = tk.Frame(
            root, height=40, highlightthickness=0)
        display_frame.pack(fill=tk.X)
        self.display_frame = display_frame

        display_label = tk.Label(display_frame, font=(font.nametofont(
            "TkDefaultFont"), 20), text="Enter your message below to generate a J-CODE")
        display_label.place(anchor="c", relx=0.5, rely=0.5)
        self.display_label = display_label

        # control
        control_frame = tk.Frame(
            root, height=80, highlightthickness=0)
        control_frame.pack(fill=tk.X)
        self.control_frame = control_frame

        widgets_frame = tk.Frame(control_frame)
        widgets_frame.place(anchor="c", relx=0.5, rely=0.5)
        self.widgets_frame = widgets_frame

        mode = tk.StringVar()
        mode.set("Encode")
        switch_mode_menu = tk.OptionMenu(
            widgets_frame, mode, "Encode", "Decode", command=self.switch_mode)
        switch_mode_menu.pack(side=tk.LEFT, padx=5)
        self.switch_mode_menu = switch_mode_menu
        self.prev_mode = "Encode"

        # content
        content_frame = tk.Frame(self.root, highlightthickness=0)
        content_frame.pack(fill=tk.BOTH, expand=True)
        self.content_frame = content_frame

        self.encoder = Encoder()
        self.image = None
        self.mount_encode_controls()
        self.mount_encode_content()

    def switch_mode(self, mode):
        if mode == "Encode" and self.prev_mode != mode:
            self.set_display_label(
                "Enter your message below to generate a J-CODE")
            self.unmount_decode_controls()
            self.unmount_decode_content()
            self.encoder = Encoder()
            self.mount_encode_controls()
            self.mount_encode_content()
        elif mode == "Decode" and self.prev_mode != mode:
            self.set_display_label("Upload your J-CODE for translation")
            self.unmount_encode_controls()
            self.unmount_encode_content()
            self.decoder = Decoder()
            self.mount_decode_controls()
            self.mount_decode_content()
        self.prev_mode = mode

    def upload_file(self):
        path = filedialog.askopenfilename(initialdir=CURRENT_DIR)
        self.decoder.add_code_path(path)
        if not path:
            self.set_display_label("No J-CODE selected")
        else:
            self.set_display_label("Uploaded J-CODE")

    def translate_code(self):
        message = self.decoder.translate_code()
        self.message_text.config(state=tk.NORMAL)
        self.message_text.delete('1.0', tk.END)
        self.message_text.insert(tk.INSERT, message)
        self.message_text.config(state=tk.DISABLED)
        self.set_display_label("Translated J-CODE")

    def mount_decode_controls(self):
        upload_code_button = tk.Button(
            self.widgets_frame, text="Upload", command=self.upload_file)
        upload_code_button.pack(side=tk.LEFT, padx=5)
        self.upload_code_button = upload_code_button

        translate_code_button = tk.Button(
            self.widgets_frame, text="Translate", command=self.translate_code)
        translate_code_button.pack(side=tk.LEFT, padx=5)
        self.translate_code_button = translate_code_button

    def unmount_decode_controls(self):
        self.upload_code_button.destroy()
        self.translate_code_button.destroy()

    def mount_decode_content(self):
        message_frame = tk.Frame(self.content_frame, width=CODE_WIDTH,
                                 height=CODE_HEIGHT, bg="blue")
        message_frame.pack_propagate(False)
        message_frame.place(anchor="c", relx=0.5, rely=0.5)
        self.message_frame = message_frame

        message_text = tk.Text(message_frame, borderwidth=0, highlightthickness=0, font=(
            font.nametofont("TkDefaultFont"), 20), state=tk.DISABLED)
        message_text.pack(fill=tk.BOTH, expand=True)
        self.message_text = message_text

    def unmount_decode_content(self):
        self.message_frame.destroy()

    def mount_encode_controls(self):
        message_frame = tk.Frame(self.widgets_frame)
        message_frame.pack(side=tk.LEFT, padx=5)
        self.message_frame = message_frame

        message_str = tk.StringVar()
        message_str.trace(
            "w", lambda *args: self._validate_message_length(message_str))
        message_entry = tk.Entry(
            message_frame, textvariable=message_str)
        message_entry.pack()
        self.message_entry = message_entry
        self.message_str = message_str

        generate_code_button = tk.Button(
            self.widgets_frame, text="Generate", command=self.generate_code)
        generate_code_button.pack(side=tk.LEFT, padx=5)
        self.generate_code_button = generate_code_button

        download_code_button = tk.Button(
            self.widgets_frame, text="Download", command=self.download_code)
        download_code_button.pack(side=tk.LEFT, padx=5)
        self.download_code_button = download_code_button

    def unmount_encode_controls(self):
        self.message_frame.destroy()
        self.generate_code_button.destroy()
        self.download_code_button.destroy()

    def mount_encode_content(self):
        code_canvas = tk.Canvas(self.content_frame, width=CODE_WIDTH,
                                height=CODE_HEIGHT, bg="red", highlightthickness=0)
        code_canvas.place(anchor="c", relx=0.5, rely=0.5)
        self.code_canvas = code_canvas
        self.render_code()

    def unmount_encode_content(self):
        self.code_canvas.destroy()

    def generate_code(self):
        message = self.message_str.get()
        self.encoder.reset()
        self.encoder.encode_message(message)
        self.render_code()
        self.set_display_label("Generated J-CODE")

    def set_display_label(self, text):
        self.display_label.config(text=text)

    def download_code(self):
        if not self.image:
            return
        self.image.save("code.png")
        self.set_display_label("Downloaded J-CODE")

    def _get_absolute_path(self, file):
        absolute_path = os.path.join(CURRENT_DIR, file)
        return absolute_path

    def _search_key_by_value_in_dict(self, dictionary, target):
        for key, val in dictionary.items():
            if val == target:
                return key

    def render_code(self):
        block_size = CODE_HEIGHT / CODE_NUM_ROWS
        image = Image.new("RGB", (CODE_WIDTH, CODE_HEIGHT))
        image_draw = ImageDraw.Draw(image)
        for row in range(CODE_NUM_ROWS):
            for col in range(CODE_NUM_COLS):
                x, y = block_size * col, block_size * row
                if (row, col) not in BLOCK_LOCATION.values():
                    self.code_canvas.create_rectangle(
                        x, y, x + block_size, y + block_size, fill=PURPLE, outline="")
                    image_draw.rectangle(
                        [(x, y), (x + block_size, y + block_size)], fill=PURPLE)
                else:
                    block_i = self._search_key_by_value_in_dict(
                        BLOCK_LOCATION, (row, col))
                    block = self.encoder.blocks[block_i]
                    square_size = block_size / BLOCK_BIT_SIZE
                    for block_row in range(BLOCK_BIT_SIZE):
                        for block_col in range(BLOCK_BIT_SIZE):
                            bx, by = square_size * block_col, square_size * block_row
                            color = "black" if block.data[block_row][block_col] == 1 else "white"
                            self.code_canvas.create_rectangle(
                                x + bx, y + by, x + bx + square_size, y + by + square_size,
                                fill=color, outline="")
                            image_draw.rectangle(
                                [(x + bx, y + by), (x + bx + square_size, y + by + square_size)], fill=color)
        self.image_draw = image_draw
        self.image = image

    def _validate_message_length(self, message_str):
        if len(message_str.get()) > MAX_MESSAGE_SIZE:
            new_message = message_str.get()[:MAX_MESSAGE_SIZE]
            message_str.set(new_message)
            self.set_display_label("Max message length reached")
        else:
            self.set_display_label(
                "Enter your message below to generate a J-CODE")

    def run(self):
        self.root.mainloop()
