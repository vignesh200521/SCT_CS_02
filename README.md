# SCT_CS_02
This Python-based GUI application allows users to encrypt and decrypt images using pixel-level transformations
Simple Image Encryption Tool (GUI)

A lightweight Python GUI application for encrypting and decrypting images using pixel manipulation techniques. This tool supports two methods: **pixel swapping** and **mathematical transformations** (add, xor, multiply). Built with `Tkinter` and `Pillow`, it's perfect for educational use, experimentation, or basic image obfuscation.


 Features
- Encrypt/Decrypt images using two distinct methods:
- Swap: Randomly swaps pixels using a seed and swap count.
  - Math: Applies mathematical operations (add, xor, mul) to pixel values.
- Live preview of the original and processed image.
- Load and save images with a simple GUI.
- Reversible encryption with correct parameters.


 Requirements
- Python 3.x
- Pillow (`pip install pillow`)


Installation

'''bash
git clone https://github.com/yourusername/image-encrypt-gui.git
cd image-encrypt-gui
python3 image_encrypt_gui.py
 Usage
- Load Image: Click "Load Image" and select a .png, .jpg, or .jpeg file.
- Choose Method:
- swap: Enter a seed and number of swaps.
- math: Choose operation (add, xor, mul) and a key (0–255).
- Encrypt or Decrypt: Click the respective button.
- Save Result: Choose where to save the processed image.
 To decrypt, use the same parameters used during encryption.




