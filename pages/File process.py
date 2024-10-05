import os
os.environ["PYTORCH_ENABLE_MPS_FALLBACK"] = "1"  # For MPS fallback

import io
import pandas as pd
import streamlit as st
from streamlit_drawable_canvas import st_canvas
import hashlib
import pypdfium2
from texify.inference import batch_inference
from texify.model.model import load_model
from texify.model.processor import load_processor
from texify.output import replace_katex_invalid
from PIL import Image
from utils.llm import generate_response  # Import LLM response function

MAX_WIDTH = 800
MAX_HEIGHT = 1000

@st.cache_resource()
def load_model_cached():
    return load_model()

@st.cache_resource()
def load_processor_cached():
    return load_processor()

@st.cache_data()
def infer_image(pil_image, bbox, temperature):
    input_img = pil_image.crop(bbox)
    model_output = batch_inference([input_img], model, processor, temperature=temperature)
    return model_output[0]

def open_pdf(pdf_file):
    stream = io.BytesIO(pdf_file.getvalue())
    return pypdfium2.PdfDocument(stream)

@st.cache_data()
def get_page_image(pdf_file, page_num, dpi=96):
    doc = open_pdf(pdf_file)
    renderer = doc.render(
        pypdfium2.PdfBitmap.to_pil,
        page_indices=[page_num - 1],
        scale=dpi / 72,
    )
    png = list(renderer)[0]
    png_image = png.convert("RGB")
    return png_image

@st.cache_data()
def get_uploaded_image(in_file):
    return Image.open(in_file).convert("RGB")

def resize_image(pil_image):
    if pil_image is None:
        return
    pil_image.thumbnail((MAX_WIDTH, MAX_HEIGHT), Image.Resampling.LANCZOS)

@st.cache_data()
def page_count(pdf_file):
    doc = open_pdf(pdf_file)
    return len(doc)

def get_canvas_hash(pil_image):
    return hashlib.md5(pil_image.tobytes()).hexdigest()

@st.cache_data()
def get_image_size(pil_image):
    if pil_image is None:
        return MAX_HEIGHT, MAX_WIDTH
    height, width = pil_image.height, pil_image.width
    return height, width

st.set_page_config(layout="wide")

# Display the instructions at the top
st.markdown("""### Texify

Upload an image or a PDF, then draw a box around the equation or text you want to OCR by clicking and dragging. Texify will convert it to Markdown with LaTeX math on the right.

### Usage Tips:
    - Try to select boxes that are neither too large nor too small.
    - Adjust the temperature for different levels of creativity.
    - If an equation doesn't render properly, it might still be valid LaTeX.
""")


# Load the model and processor
model = load_model_cached()
processor = load_processor_cached()

# File uploader for PDF or image
in_file = st.sidebar.file_uploader("PDF file or image:", type=["pdf", "png", "jpg", "jpeg", "gif", "webp"])
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

    # Process the bounding boxes and infer the text/math
    if bbox_list:
        inferences = [infer_image(pil_image, bbox, temperature) for bbox in bbox_list]
        for idx, inference in enumerate(reversed(inferences)):
            st.markdown(f"### Extracted Problem {len(inferences) - idx}")
            katex_markdown = replace_katex_invalid(inference)
            st.markdown(katex_markdown)
            st.code(inference)

            # Prompt the user to send the extracted problem to LLM for solving
            prompt = st.chat_input(f"Enter your prompt for problem {inference}:")
            if st.button('Solve Problem', key=f'solve_{idx}'):
                response = generate_response(inference)
                st.markdown(f"### Solution for Problem {len(inferences) - idx}:")
                st.write(response)

