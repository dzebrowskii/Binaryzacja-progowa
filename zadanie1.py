import numpy as np
import tkinter as tk
import matplotlib.pyplot as plt
from PIL import Image, ImageTk
from tkinter import ttk
from tkinter import filedialog
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg

class ImageProcessing:
    def __init__(self, root):
        self.root = root
        self.root.title("Image Processor")
        self.root.geometry("1000x700")

        self.image = None
        self.photo = None
        self.binarized_photo = None
        self.bin_image = None
        self.hist_canvas = None

        # Sekcja dla oryginalnego obrazu
        self.img_label_original = tk.Label(self.root, text="Original Image", width=40, height=20, relief="solid")
        self.img_label_original.grid(row=0, column=0, padx=10, pady=10, rowspan=4, sticky="nsew")

        # Sekcja dla przetworzonego obrazu
        self.img_label_binarized = tk.Label(self.root, text="Binarized Image", width=40, height=20, relief="solid")
        self.img_label_binarized.grid(row=0, column=1, padx=10, pady=10, rowspan=4, sticky="nsew")

        # Przycisk do ładowania obrazu
        self.load_btn = tk.Button(self.root, text="Load Image", command=self.load_image)
        self.load_btn.grid(row=4, column=0, padx=10, pady=10, sticky="ew")

        # Przycisk do zapisywania obrazu
        self.save_btn = tk.Button(self.root, text="Save Image", command=self.save_image)
        self.save_btn.grid(row=4, column=1, padx=10, pady=10, sticky="ew")

        # Przycisk do binaryzacji obrazu
        self.binary_btn = tk.Button(self.root, text="Binarize Image", command=self.binary_threshold)
        self.binary_btn.grid(row=5, column=0, padx=10, pady=10, sticky="ew")

        # Przycisk do wyświetlania histogramu
        self.hist_btn = tk.Button(self.root, text="Show Histogram", command=self.show_histogram)
        self.hist_btn.grid(row=5, column=1, padx=10, pady=10, sticky="ew")

        # Suwak do ustawienia progu binaryzacji
        self.threshold_slider = tk.Scale(self.root, from_=0, to=255, orient=tk.HORIZONTAL, label="Threshold")
        self.threshold_slider.grid(row=6, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Menu wyboru kanału kolorów
        self.channel_var = tk.StringVar()
        self.channel_var.set("Average")
        self.channel_menu = ttk.Combobox(self.root, textvariable=self.channel_var,
                                         values=["Red", "Green", "Blue", "Average"])
        self.channel_menu.grid(row=7, column=0, columnspan=2, padx=10, pady=10, sticky="ew")

        # Miejsce na histogram
        self.hist_frame = tk.Frame(self.root, relief="solid", borderwidth=1)
        self.hist_frame.grid(row=0, column=2, rowspan=8, padx=10, pady=10, sticky="nsew")

        # Dynamiczne skalowanie elementów w pionie i poziomie
        self.root.grid_columnconfigure(0, weight=1)
        self.root.grid_columnconfigure(1, weight=1)
        self.root.grid_rowconfigure(0, weight=1)



    def load_image(self):
        file_path = filedialog.askopenfilename()
        if file_path:
            self.image = Image.open(file_path).convert('RGB')
            self.photo = ImageTk.PhotoImage(self.image)
            self.img_label_original.config(image=self.photo)


    def save_image(self):
        if self.bin_image:
            save_path = filedialog.asksaveasfilename(defaultextension=".png")
            if save_path:
                self.bin_image.save(save_path)
        pass

    def binary_threshold(self):

        if self.image:
            threshold = self.threshold_slider.get()
            channel = self.channel_var.get()

            image_array = np.array(self.image)

            if channel == 'Red':
                binary_image = (image_array[:, :, 0] > threshold) * 255

            elif channel == 'Green':
                binary_image = (image_array[:, :, 1] > threshold) * 255

            elif channel == 'Blue':
                binary_image = (image_array[:, :, 2] > threshold) * 255

            else:
                binary_image = (image_array.mean(axis=2) > threshold) * 255

            binary_image = binary_image.astype(np.uint8)
            self.bin_image = Image.fromarray(binary_image)
            self.binarized_photo = ImageTk.PhotoImage(self.bin_image)
            self.img_label_binarized.config(image=self.binarized_photo)



    def show_histogram(self):
        if self.image:
            image_array = np.array(self.image)
            channel = self.channel_var.get()

            if channel == 'Red':
                histogram_data = image_array[:, :, 0].flatten()
                color = 'red'

            elif channel == 'Green':
                histogram_data = image_array[:, :, 1].flatten()
                color = 'green'

            elif channel == 'Blue':
                histogram_data = image_array[:, :, 2].flatten()
                color = 'blue'

            else:
                histogram_data = image_array.mean(axis=2).flatten()
                color = 'black'

            fig, ax = plt.subplots(figsize=(4, 4))
            ax.hist(histogram_data, bins=256, range=(0, 255), color=color)
            ax.set_title(f"Histogram - {channel} channel")
            ax.set_xlabel("Pixel value")
            ax.set_ylabel("Frequency")

            # Usuwanie poprzedniego wykresu z okna
            if self.hist_canvas:
                self.hist_canvas.get_tk_widget().destroy()

            # Osadzenie wykresu w Tkinterze
            self.hist_canvas = FigureCanvasTkAgg(fig, master=self.hist_frame)
            self.hist_canvas.draw()
            self.hist_canvas.get_tk_widget().pack()


if __name__ == '__main__':
    root = tk.Tk()
    app = ImageProcessing(root)
    root.mainloop()

