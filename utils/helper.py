import requests
import os
from PIL import Image
import easyocr
import g4f
from g4f.client import Client
import numpy as np
import cv2
from PIL import Image
# from dotenv import load_env

# load_env()


# Ensure you've set up your Hugging Face API token in your environment variables
HuggingFace = os.environ["HuggingFace"]

def solve_math_problem(problem):
    # Placeholder for O1 model integration
    try:
        client = Client()
        response = client.chat.completions.create(
            model=g4f.models.gpt_4o,
            messages=[{'role': 'user', 'content': problem}]
        )
        response = response.choices[0].message.content
        return response
    except Exception as e:
        return f"Error: {str(e)}"

def process_whiteboard_image(image):
    # Convert PIL image to OpenCV format
    open_cv_image = np.array(image)
    gray_image = cv2.cvtColor(open_cv_image, cv2.COLOR_BGR2GRAY)
    
    # Apply threshold to improve contrast
    _, thresh_image = cv2.threshold(gray_image, 150, 255, cv2.THRESH_BINARY_INV)

    # Save the preprocessed image for debugging
    cv2.imwrite("/mnt/data/preprocessed_image.png", thresh_image)
    
    # Initialize EasyOCR reader
    reader = easyocr.Reader(['en', 'la'])

    # Use EasyOCR to perform OCR on the preprocessed image
    result = reader.readtext(thresh_image)

    # Extract text from result
    extracted_text = ' '.join([item[1] for item in result])

    # Clean up the text (remove extra spaces, etc.)
    cleaned_text = ' '.join(extracted_text.split())

    return cleaned_text


# Math symbols for the advanced keyboard
MATH_SYMBOLS = [
    '√', 'π', '∑', '∫', '∂', '∞', '±', '≠', '≤', '≥',
    '∈', '∉', '∩', '∪', '⊂', '⊃', '⊄', '⊅', '∀', '∃',
    '→', '←', '↔', '⇒', '⇐', '⇔', '∧', '∨', '¬', '⊕',
    'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'lim', 'sup', 'inf', 'max'
]