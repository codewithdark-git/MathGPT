# ===========================================
# White-Board functionality logic and equation recognition
# ===========================================

import streamlit as st
import numpy as np
from PIL import Image
from texify.inference import batch_inference
from texify.output import replace_katex_invalid
from streamlit_drawable_canvas import st_canvas
from utils.load_model import load_modelANDprocessor
from utils.llm import generate_response
from utils.prompting import prompt_WB, prompt_StepByStep


# Load the model and processor
model, processor = load_modelANDprocessor()

@st.cache_data()
def infer_whole_image(pil_image, temperature):
    # Use the entire image for inference by setting bbox to the full image dimensions
    bbox = (0, 0, pil_image.width, pil_image.height)
    model_output = batch_inference([pil_image.crop(bbox)], model, processor, temperature=temperature)
    return model_output[0]

# Process whiteboard image function
def process_whiteboard_image(image, temperature=0.7):
    # Process the entire whiteboard image (no bounding box needed)
    output = infer_whole_image(image, temperature)
    extract_text = replace_katex_invalid(output)
    return extract_text


def main():
    st.header("Whiteboard Math Problem Solver")
    
    
    st.markdown("""
    **Instructions:**
    1. Use the whiteboard below to draw a mathematical equation.
    2. Click "Solve from Whiteboard" to extract and solve the equation.
    3. Wait for the solution to appear below.
    """)

    # Streamlit Drawing Component for whiteboard simulation
    canvas_result = st_canvas(
                                    fill_color="rgba(255, 165, 0, 0.1)",  # Light orange background fill color with some transparency
                                    stroke_width=2,  # Set the stroke width for drawing medium-sized text
                                    stroke_color="#000000",  # Black stroke for clarity
                                    background_color="#FFFFFF",  # White background
                                    height=400,  # Adjust the canvas height for appropriate scaling (increase from 300)
                                    width=700,  # Keep the width the same
                                    drawing_mode="freedraw",  # Allows freehand drawing (you can use 'rect' for bounding box)
                                    key="canvas",
                                )
    
    if st.button("Solve from Whiteboard"):
        if canvas_result.image_data is not None:
            st.write("Processing the whiteboard image...")

            # Convert the drawn canvas into an image and process it
            image = Image.fromarray(canvas_result.image_data.astype(np.uint8))
            
            # Process the whiteboard image to extract the equation
            problem = process_whiteboard_image(image)
            
            st.write("Detected problem:", problem)
            
            # Solve the detected math problem using the LLM
            solution = prompt_WB(problem)
            fin_response = generate_response(solution)
            st.write("Solution:", fin_response)
        else:
            st.write("Please draw something on the whiteboard first.")


if __name__ == "__main__":
    main()
