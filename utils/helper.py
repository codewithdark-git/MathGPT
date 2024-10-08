# ######################################################
#                                                      #
#          This file contains all helper functions     #
#                  for the application.                #
#                                                      #
# ######################################################


import io
import hashlib
import pypdfium2
from PIL import Image
import streamlit as st
import latex2mathml.converter
from utils.symbols import MATH_SYMBOLS
from texify.inference import batch_inference
from texify.output import replace_katex_invalid
from utils.load_model import load_modelANDprocessor

MAX_WIDTH = 800
MAX_HEIGHT = 1000

# Load the model and processor
model, processor = load_modelANDprocessor()


def render_latex(latex):
    return latex2mathml.converter.convert(latex)

def symbol_button(symbol, key):
    if st.button(symbol, key=key, help=f"Insert {symbol}"):
        st.session_state.math_input = st.session_state.get('math_input', '') + symbol

def math_keyboard():
    st.write("**Math Keyboard**")
    with st.expander('Math Keyboard Symbols'):
        categories = list(MATH_SYMBOLS.keys())
        tabs = st.tabs(categories)

        for tab, category in zip(tabs, categories):
            with tab:
                symbols = MATH_SYMBOLS[category]
                cols = st.columns(8)
                for i, symbol in enumerate(symbols):
                    with cols[i % 8]:
                        symbol_button(symbol, f"{category}_{symbol}")



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