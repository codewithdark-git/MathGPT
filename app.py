import streamlit as st
from utils.llm import generate_response
from utils.symbols import MATH_SYMBOLS
from utils.plotting import plot_function
import latex2mathml.converter
from streamlit_drawable_canvas import st_canvas
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt

# CSS for custom UI styling
def add_custom_css():
    st.markdown("""
        <style>
            body {
                font-family: 'Arial', sans-serif;
                background-color: #f0f0f5;
            }
            .stButton>button {
                background-color: #4CAF50;
                color: white;
                border: none;
                padding: 10px 20px;
                border-radius: 5px;
            }
            .stButton>button:hover {
                background-color: #45a049;
            }
            .stTextInput>div>input {
                border: 1px solid #ccc;
                border-radius: 5px;
                padding: 10px;
            }
            .main-title {
                font-size: 32px;
                color: #333;
                text-align: center;
                font-weight: bold;
                margin-bottom: 20px;
            }
            .main-container {
                background-color: #fff;
                padding: 20px;
                border-radius: 10px;
                box-shadow: 0 4px 8px rgba(0, 0, 0, 0.1);
            }
        </style>
    """, unsafe_allow_html=True)

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

# Function to plot drawable whiteboard and math input
def draw_whiteboard():
    st.header("Whiteboard")
    
    # Initialize drawable canvas
    canvas_result = st_canvas(
        fill_color="rgba(255, 165, 0, 0.1)",
        stroke_width=2,
        background_color="#fff",
        height=200,
        width=700,
        drawing_mode="freedraw",
        point_display_radius=0,
        update_streamlit=True,
        key="canvas"
    )

    if canvas_result.image_data is not None:
        st.image(canvas_result.image_data)
    
    return canvas_result.image_data

# Enhanced math input page
def math_input_page():
    st.write('<div class="main-title">Advanced Math Problem Solver</div>', unsafe_allow_html=True)
    st.write('<div class="main-container">', unsafe_allow_html=True)

    st.write("""
    Welcome to the Advanced Math Problem Solver! Here's how to use this app:
    1. Write your problem on the whiteboard or use 'Text Input' or 'LaTeX Input' tabs.
    2. Use the Math Keyboard to easily input mathematical symbols.
    3. Click 'Solve' to get the solution or 'Plot Function' to visualize it.
    """)

    draw_whiteboard()

    math_keyboard()

    # Tabs for different input methods
    tab1, tab2 = st.tabs(["Text Input", "LaTeX Input"])

    with tab1:
        math_input = st.text_input("Enter your math problem:", value=st.session_state.get('math_input', ''),
                                help="Type or use the Math Keyboard to input your problem")
        st.session_state.math_input = math_input

    with tab2:
        latex_input = st.text_area("Enter LaTeX:", value=st.session_state.get('latex_input', ''),
                                help="Enter your mathematical expression in LaTeX format")
        st.session_state.latex_input = latex_input
        if latex_input:
            st.write("Preview:")
            st.write(render_latex(latex_input))

    solve_col, plot_col = st.columns(2)
    with solve_col:
        solve_button = st.button("Solve", help="Click to solve the problem", use_container_width=True)
    with plot_col:
        plot_button = st.button("Plot Function", help="Click to plot the function", use_container_width=True)

    if solve_button:
        input_to_solve = math_input if tab1 else latex_input
        if input_to_solve:
            with st.spinner("Solving the problem..."):
                solution = generate_response(input_to_solve)
                st.subheader("Solution:")
                st.write(solution)

                # Try to render the solution as LaTeX
                try:
                    st.write("LaTeX rendering:")
                    st.write(render_latex(solution))
                except:
                    st.write("(Unable to render solution as LaTeX)")

                # Offer step-by-step explanation
                if st.button("Show step-by-step explanation"):
                    explanation = generate_response(f"Explain the solution to {input_to_solve} step by step")
                    st.write(explanation)
        else:
            st.warning("Please enter a math problem first.")

    if plot_button:
        input_to_plot = math_input if tab1.active else latex_input
        if input_to_plot:
            fig = plot_function(input_to_plot)
            if fig:
                st.pyplot(fig)
        else:
            st.warning("Please enter a function to plot.")

    # History feature
    if 'history' not in st.session_state:
        st.session_state.history = []

    if solve_button or plot_button:
        current_problem = math_input if tab1 else latex_input
        st.session_state.history.append(current_problem)

    with st.expander("Problem History"):
        if st.session_state.history:
            for i, problem in enumerate(st.session_state.history):
                st.write(f"{i + 1}. {problem}")
        else:
            st.write("No problems solved yet. Your history will appear here.")

    st.write('</div>', unsafe_allow_html=True)

def main():
    st.set_page_config(page_title="Advanced Math Problem Solver", page_icon="🧮", layout="wide")
    add_custom_css()
    math_input_page()

    # Sidebar for settings and info
    with st.sidebar:
        st.subheader("Settings")
        st.selectbox("Theme", ["Light", "Dark"], help="Choose the app theme")
        st.checkbox("Enable animations", help="Toggle animations in the app")

        st.subheader("About")
        st.info("This app uses advanced AI to solve and explain mathematical problems. It can handle a wide range of topics including algebra, calculus, and more.")

        st.subheader("Feedback")
        feedback = st.text_area("Leave your feedback here:", help="We appreciate your feedback!")
        if st.button("Submit Feedback"):
            st.success("Thank you for your feedback!")

if __name__ == "__main__":
    main()
