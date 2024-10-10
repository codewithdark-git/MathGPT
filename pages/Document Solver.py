import os

from utils.load_model import load_modelANDprocessor
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"  # For MPS fallback


import time
import pandas as pd
import streamlit as st

from texify.output import replace_katex_invalid
from streamlit_drawable_canvas import st_canvas

from utils.load_model import load_modelANDprocessor
from utils.llm import generate_response
from utils.prompting import prompt_FP
from utils.helper import (
    infer_image,
    get_image_size,
    get_canvas_hash,
    get_page_image,
    get_uploaded_image,
    page_count,
    resize_image,
)



st.markdown(
        """
        <style>
        .title {
            font-size: 30px;
            font-weight: lighter;
            color: #333;  /* Optional: Change color */
            text-align: center;
            margin-top: 0px;
        }
        </style>
        """, unsafe_allow_html=True)
    
st.markdown('<div class="title">Document Solver</div>', unsafe_allow_html=True)
st.divider()
st.write('Choose Your Choice 🪧:')
col1, col2, col3 = st.columns(3)
with col1:
    st.page_link('app.py', label='Back To Home', icon="🏠")
with col2:
    st.page_link('pages/QuickSolve.py', label='QuickSolve', icon="🕒")
with col3:
    st.page_link('pages/Math Sketchboard.py', label='Math Sketchboard', icon="⬜")

st.divider()

# Display the instructions at the top
st.markdown("""
**Upload an image or a PDF file** containing mathematical problems or text. After uploading, the system will automatically process the file and Draw Shape on Equation, for extract the relevant math equations or text using OCR technology. The extracted content will then be converted to readable Markdown with LaTeX formatting for further solution generation.
### Usage Tips:
    - Try to select boxes that are neither too large nor too small.
    - Adjust the temperature for different levels of creativity.
    - If an equation doesn't render properly, it might still be valid LaTeX.
""")


# Load the model and processor
model , processor = load_modelANDprocessor()

# File uploader for PDF or image
in_file = st.file_uploader("PDF file or image:", type=["pdf", "png", "jpg", "jpeg", "gif", "webp"])
if in_file is None:
    st.stop()

# Determine file type and process the file
filetype = in_file.type
if "pdf" in filetype:
    total_pages = page_count(in_file)
    page_number = st.sidebar.number_input(f"Page number out of {total_pages}:", min_value=1, value=1, max_value=total_pages)
    pil_image = get_page_image(in_file, page_number)
else:
    pil_image = get_uploaded_image(in_file)

# Resize the image
resize_image(pil_image)

# Static temperature value
temperature = 0.7  # Static temperature instead of slider

# Create a unique hash for the canvas
canvas_hash = get_canvas_hash(pil_image) if pil_image else "canvas"

# Create the canvas component
canvas_result = st_canvas(
    fill_color="rgba(255, 165, 0, 0.1)",  # Fixed fill color with some opacity
    stroke_width=1,
    stroke_color="#FFAA00",
    background_color="#FFF",
    background_image=pil_image,
    update_streamlit=True,
    height=get_image_size(pil_image)[0],
    width=get_image_size(pil_image)[1],
    drawing_mode="rect",
    point_display_radius=0,
    key=canvas_hash,
)

# Extract the bounding box and inference if available
if canvas_result.json_data is not None:
    objects = pd.json_normalize(canvas_result.json_data["objects"])
    bbox_list = None
    if objects.shape[0] > 0:
        boxes = objects[objects["type"] == "rect"][["left", "top", "width", "height"]]
        boxes["right"] = boxes["left"] + boxes["width"]
        boxes["bottom"] = boxes["top"] + boxes["height"]
        bbox_list = boxes[["left", "top", "right", "bottom"]].values.tolist()


    # user input for question
    user_input = st.chat_input('Tell me what you want to do with this question')
    # Process the bounding boxes and infer the text/math
    if bbox_list and user_input:
        
        with st.status("Analyzing...", expanded=True) as status:
            # Run inference and generate response inside the expander
            st.write('Extracting math problems from the image... 🔍')
            inferences = [infer_image(pil_image, bbox, temperature) for bbox in bbox_list]
            st.write('Thinking and analyzing the math problems...')
            time.sleep(2)

            st.write('Generating the solution for the extracted problems... 💡')
            solution = prompt_FP(user_input, inferences)
            st.write('Calculating and generating the best solution...')
            
            fin_response = generate_response(solution)

            status.update(
                label="Analysis Complete!", state="complete", expanded=False
            )

        # Display extracted problems outside of expander
        for idx, inference in enumerate(reversed(inferences)):
            st.markdown(f"### Extracted Problem {len(inferences) - idx}")
            katex_markdown = replace_katex_invalid(inference)
            st.markdown(katex_markdown)
            st.code(inference)

        # Display the final solution outside of the expander
        st.markdown(f"Solution: {fin_response}")
        st.divider()
