import cv2
import numpy as np
from PIL import Image
import pytesseract
import re
from pix2tex.cli import LatexOCR as BaseLatexOCR
import io
import os
import torch

# Add this line near the top of your file, after the imports
pytesseract.pytesseract.tesseract_cmd = r'C:\Program Files\Tesseract-OCR\tesseract.exe'

def preprocess_image(image_path):
    # Read the image
    img = cv2.imread(image_path)
    
    # Convert to grayscale
    gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
    
    # Apply thresholding to preprocess the image
    gray = cv2.threshold(gray, 0, 255, cv2.THRESH_BINARY | cv2.THRESH_OTSU)[1]
    
    # Apply dilation to connect text components
    kernel = np.ones((2,2), np.uint8)
    gray = cv2.dilate(gray, kernel, iterations=1)
    
    return Image.fromarray(gray)

class CustomLatexOCR(BaseLatexOCR):
    def load_model(self):
        self.model.load_state_dict(torch.load(self.args.checkpoint, map_location=self.args.device, weights_only=True))
        if os.path.exists(os.path.join(os.path.dirname(self.args.checkpoint), 'image_resizer.pth')):
            self.image_resizer.load_state_dict(torch.load(os.path.join(os.path.dirname(self.args.checkpoint), 'image_resizer.pth'), map_location=self.args.device, weights_only=True))

def equation_to_text():
    image_path = r"C:\Users\moizu\OneDrive\Desktop\Project Related\Python\Self Projects\MathToFunction\Opera Snapshot_2024-10-26_182303_www.google.com.png"
    
    # Use the custom LatexOCR class
    model = CustomLatexOCR()
    latex_equation = model(Image.open(image_path))
    
    return f"Detected LaTeX equation: {latex_equation}"

def convert_to_verbal(equation):
    # This is a simple conversion, you may need to expand it
    equation = equation.replace('+', ' plus ')
    equation = equation.replace('-', ' minus ')
    equation = equation.replace('*', ' times ')
    equation = equation.replace('/', ' divided by ')
    equation = equation.replace('=', ' equals ')
    return equation

def process_equation_image(image_path):
    if not image_path.lower().endswith('.jpg') and not image_path.lower().endswith('.jpeg'):
        return "Please provide a JPEG image file."
    
    try:
        result = equation_to_text(image_path)
        return result
    except Exception as e:
        return f"An error occurred while processing the image: {str(e)}"

# Add this at the end of the file
if __name__ == "__main__":
    result = equation_to_text()
    print(result)
