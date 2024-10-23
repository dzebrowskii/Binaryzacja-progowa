import numpy as np
import tkinter as tk
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog

class ImageProcessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("800x600")

        self.image = None
        self.photo = None
        self.img_label = tk.Label(self.root)
        self.img_label.pack()

        self.load_btn = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_btn.pack(side=tk.LEFT, padx=10)

        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_btn.pack(side=tk.LEFT, padx=10)

        self.binary_btn = tk.Button(self.root, text="Binarize Image", command=self.binary_threshold)
        self.binary_btn.pack(side=tk.LEFT, padx=10)

        self.hist_btn = tk.Button(self.root, text="Show Histogram", command=self.show_histogram)
        self.hist_btn.pack(side=tk.LEFT, padx=10)

        self.threshold_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold")
        self.threshold_slider.pack(side=tk.BOTTOM, pady=10)

        self.channel_var = tk.StringVar()
        self.channel_var.set("Average")
        self.channel_menu = ttk.Combobox(self.root, textvariable=self.channel_var, values=["Red", "Green", "Blue", "Average"])
        self.channel_menu.pack(side=tk.BOTTOM)



    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path)
            self.photo = ImageTk.PhotoImage(self.image)
            self.img_label.config(image=self.photo)

    def save_image(self):
        if self.image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                self.image.save(save_path)
        pass

    def binary_threshold(self):
        if self.image:
            threshold = self.threshold_slider.get()
            channel = self.channel_var.get()

            image_array = np.array(self.image)

            if channel == 'Red':
                image_array[]





    def show_histogram(self):
        pass

    def apply_threshold(self):
        pass



if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessing(root)
    root.mainloop()

