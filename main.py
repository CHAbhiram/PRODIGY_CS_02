import numpy as np
from PIL import Image
import tkinter as tk
from tkinter import filedialog, messagebox
import os

class ImageEncryptorDecryptor:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Encryptor and Decryptor")
        
        self.image_path = None
        self.key_path = "encryption_key.npy"

        self.label = tk.Label(root, text="Select an image to encrypt or decrypt")
        self.label.pack(pady=10)

        self.select_button = tk.Button(root, text="Select Image", command=self.select_image)
        self.select_button.pack(pady=10)

        self.encrypt_button = tk.Button(root, text="Encrypt Image", command=self.encrypt_image, state=tk.DISABLED)
        self.encrypt_button.pack(pady=10)

        self.decrypt_button = tk.Button(root, text="Decrypt Image", command=self.decrypt_image, state=tk.DISABLED)
        self.decrypt_button.pack(pady=10)

    def select_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png;*.jpg;*.jpeg;*.bmp;*.tiff")])
        if self.image_path:
            self.label.config(text=f"Selected image: {self.image_path.split('/')[-1]}")
            self.encrypt_button.config(state=tk.NORMAL)
            self.decrypt_button.config(state=tk.NORMAL)

    def generate_key(self, image_shape):
        key = np.random.randint(0, 256, size=image_shape, dtype=np.uint8)
        np.save(self.key_path, key)
        return key

    def load_key(self):
        if os.path.exists(self.key_path):
            return np.load(self.key_path)
        else:
            messagebox.showerror("Error", "Key file not found.")
            return None

    def encrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return

        img = Image.open(self.image_path)
        img = img.convert("RGB")
        img_array = np.array(img)

        key = self.generate_key(img_array.shape)

        key = np.resize(key, img_array.shape)
        encrypted_array = np.bitwise_xor(img_array, key)
        encrypted_img = Image.fromarray(encrypted_array)
        encrypted_img.save("encrypted_image.png")

        messagebox.showinfo("Success", "Image encrypted successfully.")
        self.decrypt_button.config(state=tk.NORMAL)

    def decrypt_image(self):
        if not self.image_path:
            messagebox.showerror("Error", "No image selected.")
            return

        encrypted_img = Image.open(self.image_path)
        encrypted_img = encrypted_img.convert("RGB")
        encrypted_array = np.array(encrypted_img)

        key = self.load_key()
        if key is None:
            return

        key = np.resize(key, encrypted_array.shape)
        decrypted_array = np.bitwise_xor(encrypted_array, key)
        decrypted_img = Image.fromarray(decrypted_array)
        decrypted_img.save("decrypted_image.png")

        messagebox.showinfo("Success", "Image decrypted successfully.")

def main():
    root = tk.Tk()
    app = ImageEncryptorDecryptor(root)
    root.mainloop()

if __name__ == "__main__":
    main()
