from texify.model.model import load_model
from texify.model.processor import load_processor
import streamlit as st

@st.cache_resource()
def load_modelANDprocessor():
    return load_model(), load_processor()
