#!/usr/bin/env python3
import tkinter as tk
from tkinter import filedialog, messagebox
from PIL import Image, ImageTk
import random
import os


def load_image_pixels(path):
    img = Image.open(path).convert("RGBA")
    w, h = img.size
    pixels = list(img.getdata())
    return img, (w, h), pixels

def save_image_pixels(mode, size, pixels, out_path):
    img = Image.new(mode, size)
    img.putdata(pixels)
    img.save(out_path)

def swap_pixels(pixels, seed, n_swaps, reverse=False):
    rng = random.Random(seed)
    swaps = []
    N = len(pixels)

    for _ in range(n_swaps):
        i = rng.randrange(N)
        j = rng.randrange(N)
        swaps.append((i, j))

    if reverse:
        swaps = reversed(swaps)

    pixels = pixels[:]
    for i, j in swaps:
        pixels[i], pixels[j] = pixels[j], pixels[i]
    return pixels

def math_transform(pixels, op, key, reverse=False):
    if not (0 <= key <= 255):
        raise ValueError("Key must be 0–255")

    def inv(k):
        try:
            return pow(k, -1, 256)
        except:
            raise ValueError("Multiply key must be odd to decrypt.")

    if reverse:
        if op == "add": func = lambda b: (b - key) % 256
        elif op == "xor": func = lambda b: b ^ key
        elif op == "mul": func = lambda b: (b * inv(key)) % 256
    else:
        if op == "add": func = lambda b: (b + key) % 256
        elif op == "xor": func = lambda b: b ^ key
        elif op == "mul": func = lambda b: (b * key) % 256

    out = []
    for px in pixels:
        out.append(tuple(func(c) for c in px))
    return out


class ImageEncryptGUI:
    def __init__(self, root):  # Fixed constructor name
        self.root = root
        root.title("Simple Image Encryption Tool (GUI)")

        self.image_path = None
        self.img_preview = None

        # Frame layout
        frame = tk.Frame(root, padx=10, pady=10)
        frame.pack()

        # Load button
        tk.Button(frame, text="Load Image", command=self.load_image).grid(row=0, column=0)

        # Method dropdown
        tk.Label(frame, text="Method:").grid(row=1, column=0, sticky="w")
        self.method_var = tk.StringVar(value="swap")
        tk.OptionMenu(frame, self.method_var, "swap", "math").grid(row=1, column=1)

        # Swap method params
        tk.Label(frame, text="Seed:").grid(row=2, column=0, sticky="w")
        self.seed_entry = tk.Entry(frame)
        self.seed_entry.insert(0, "12345")
        self.seed_entry.grid(row=2, column=1)

        tk.Label(frame, text="Swaps:").grid(row=3, column=0, sticky="w")
        self.swaps_entry = tk.Entry(frame)
        self.swaps_entry.insert(0, "50000")
        self.swaps_entry.grid(row=3, column=1)

        # Math method params
        tk.Label(frame, text="Op (add/xor/mul):").grid(row=4, column=0, sticky="w")
        self.op_entry = tk.Entry(frame)
        self.op_entry.insert(0, "add")
        self.op_entry.grid(row=4, column=1)

        tk.Label(frame, text="Key (0–255):").grid(row=5, column=0, sticky="w")
        self.key_entry = tk.Entry(frame)
        self.key_entry.insert(0, "42")
        self.key_entry.grid(row=5, column=1)

        # Encrypt / Decrypt buttons
        tk.Button(frame, text="Encrypt", command=self.encrypt).grid(row=6, column=0)
        tk.Button(frame, text="Decrypt", command=self.decrypt).grid(row=6, column=1)

        # Canvas for preview
        self.canvas = tk.Canvas(root, width=400, height=400, bg="black")
        self.canvas.pack(pady=10)

    def load_image(self):
        path = filedialog.askopenfilename(filetypes=[("Images", "*.png *.jpg *.jpeg")])
        if not path:
            return
        self.image_path = path
        self.display_image(path)

    def display_image(self, path):
        img = Image.open(path)
        img.thumbnail((400, 400))
        self.img_preview = ImageTk.PhotoImage(img)
        self.canvas.create_image(200, 200, image=self.img_preview)

    def get_params(self):
        method = self.method_var.get()
        seed = int(self.seed_entry.get())
        swaps = int(self.swaps_entry.get())
        op = self.op_entry.get()
        key = int(self.key_entry.get())
        return method, seed, swaps, op, key

    def process(self, decrypt=False):
        if not self.image_path:
            messagebox.showerror("Error", "No image loaded.")
            return

        method, seed, swaps, op, key = self.get_params()
        img, size, pixels = load_image_pixels(self.image_path)

        try:
            if method == "swap":
                out_pix = swap_pixels(pixels, seed, swaps, reverse=decrypt)
            elif method == "math":
                out_pix = math_transform(pixels, op, key, reverse=decrypt)
            else:
                raise ValueError("Invalid method.")
        except Exception as e:
            messagebox.showerror("Processing Error", str(e))
            return

        out_path = filedialog.asksaveasfilename(defaultextension=".png",
                filetypes=[("PNG", "*.png")])
        if not out_path:
            return

        save_image_pixels("RGBA", size, out_pix, out_path)
        self.display_image(out_path)
        messagebox.showinfo("Success", f"Saved: {out_path}")

    def encrypt(self):
        self.process(decrypt=False)

    def decrypt(self):
        self.process(decrypt=True)


if __name__ == "__main__":  # Fixed entry point
    root = tk.Tk()
    app = ImageEncryptGUI(root)
    root.mainloop()
                           
