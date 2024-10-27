import tkinter as tk
from tkinter import filedialog
from PIL import Image, ImageTk
import sys
import os

# Add the parent directory to sys.path to import PictureToLatex
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from PictureToLatex import CustomLatexOCR, equation_to_text

class UserInputPic:
    def __init__(self, master):
        self.master = master
        self.master.title("Math Equation Image Input")
        
        self.canvas = tk.Canvas(master, width=400, height=400)
        self.canvas.pack()

        self.upload_button = tk.Button(master, text="Upload Image", command=self.upload_image)
        self.upload_button.pack()

        self.process_button = tk.Button(master, text="Process Image", command=self.process_image, state=tk.DISABLED)
        self.process_button.pack()

        self.result_label = tk.Label(master, text="", wraplength=380)
        self.result_label.pack()

        self.image_path = None

    def upload_image(self):
        self.image_path = filedialog.askopenfilename(filetypes=[("Image files", "*.png *.jpg *.jpeg *.bmp *.gif")])
        if self.image_path:
            image = Image.open(self.image_path)
            image.thumbnail((400, 400))
            photo = ImageTk.PhotoImage(image)
            self.canvas.create_image(200, 200, image=photo)
            self.canvas.image = photo
            self.process_button['state'] = tk.NORMAL

    def process_image(self):
        if self.image_path:
            model = CustomLatexOCR()
            latex_equation = model(Image.open(self.image_path))
            result = f"Detected LaTeX equation: {latex_equation}"
            self.result_label.config(text=result)

if __name__ == "__main__":
    root = tk.Tk()
    app = UserInputPic(root)
    root.mainloop()
