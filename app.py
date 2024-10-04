import streamlit as st
import numpy as np
from PIL import Image
import cv2
import g4f
from g4f.client import Client
import os
from streamlit_drawable_canvas import st_canvas
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor


# Math symbols for the advanced keyboard
MATH_SYMBOLS = [
    '√', 'π', '∑', '∫', '∂', '∞', '±', '≠', '≤', '≥',
    '∈', '∉', '∩', '∪', '⊂', '⊃', '⊄', '⊅', '∀', '∃',
    '→', '←', '↔', '⇒', '⇐', '⇔', '∧', '∨', '¬', '⊕',
    'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'lim', 'sup', 'inf', 'max'
]

@st.cache_resource
def load_texify_model():
    return load_model(), load_processor()

def solve_math_problem(problem):
    try:
        client = Client()
        response = client.chat.completions.create(
            model=g4f.models.gpt_4,
            messages=[{'role': 'user', 'content': f"Solve this math problem step by step: {problem}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def preprocess_image(image):
    # Convert to grayscale
    gray = cv2.cvtColor(image, cv2.COLOR_RGB2GRAY)
    
    # Apply Gaussian blur to reduce noise
    blurred = cv2.GaussianBlur(gray, (5, 5), 0)
    
    # Apply adaptive thresholding
    thresh = cv2.adaptiveThreshold(blurred, 255, cv2.ADAPTIVE_THRESH_GAUSSIAN_C, cv2.THRESH_BINARY_INV, 11, 2)
    
    # Perform morphological operations
    kernel = np.ones((3,3), np.uint8)
    opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel, iterations=1)
    
    return opening

def process_whiteboard_image(image):
    open_cv_image = np.array(image)
    
    # Preprocess the image
    processed_image = preprocess_image(open_cv_image)
    
    # Save the preprocessed image for debugging
    cv2.imwrite("preprocessed_image.png", processed_image)
    
    # Convert back to PIL Image for Texify
    pil_image = Image.fromarray(processed_image)
    
    # Use Texify for equation recognition
    model, processor = load_texify_model()
    results = batch_inference([pil_image], model, processor)
    
    # The result is typically LaTeX code
    latex_equation = results[0] if results else ""
    
    return latex_equation

def whiteboard_page():
    st.header("Whiteboard")
    
    canvas_result = st_canvas(
        fill_color="rgba(0, 0, 0, 1)",  # Black color for better contrast
        stroke_width=5,
        background_color="#FFFFFF",
        height=400,
        width=800,
        drawing_mode="freedraw",
        key="canvas",
    )
    
    if st.button("Solve from Whiteboard"):
        if canvas_result.image_data is not None:
            with st.spinner("Processing the whiteboard image..."):
                image = Image.fromarray(canvas_result.image_data.astype(np.uint8), 'RGBA').convert('RGB')
                latex_equation = process_whiteboard_image(image)
                
                st.write("Detected LaTeX equation:", latex_equation)
                
                # Display the preprocessed image
                st.image("preprocessed_image.png", caption="Preprocessed Image", use_column_width=True)
                
                with st.spinner("Solving the problem..."):
                    solution = solve_math_problem(latex_equation)
                    st.write("Solution:", solution)
        else:
            st.warning("Please draw something on the whiteboard first.")

def math_input_page():
    st.header("Math Input")
    
    with st.expander("Math Keyboard"):
        st.subheader("Advanced Math Keyboard")
        cols = st.columns(10)
        for i, symbol in enumerate(MATH_SYMBOLS):
            if cols[i % 10].button(symbol):
                st.session_state.math_input = st.session_state.get('math_input', '') + symbol

    math_input = st.text_input("Enter your math problem:", value=st.session_state.get('math_input', ''))
    st.session_state.math_input = math_input

    if st.button("Solve"):
        if math_input:
            with st.spinner("Solving the problem..."):
                solution = solve_math_problem(math_input)
                st.write("Solution:", solution)
        else:
            st.warning("Please enter a math problem first.")

def main():
    st.set_page_config(page_title="Advanced Math Problem Solver", page_icon="🧮", layout="wide")
    st.title("Advanced Math Problem Solver")

    page = st.sidebar.selectbox("Choose a feature", ["Whiteboard", "Math Input"])

    if page == "Whiteboard":
        whiteboard_page()
    elif page == "Math Input":
        math_input_page()

if __name__ == "__main__":
    main()