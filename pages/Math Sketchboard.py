# ===========================================
# White-Board functionality logic and equation recognition
# ===========================================

import streamlit as st
import numpy as np
from PIL import Image
from streamlit_drawable_canvas import st_canvas
from utils.llm import generate_response
from utils.prompting import prompt_WB





def main():
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
    
    st.markdown('<div class="title">Whiteboard Math Problem Solver</div>', unsafe_allow_html=True)
    st.divider()
    st.write('Choose Your Choice 🪧:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link('app.py', label='Back To Home', icon="🏠")
    with col2:
        st.page_link('pages/QuickSolve.py', label='QuickSolve', icon="🕒")
    with col3:
        st.page_link('pages/Document Solver.py', label='Document Solver', icon="⬜")


    st.divider()
    
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
