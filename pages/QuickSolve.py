import scipy as sp
import streamlit as st
from utils.llm import generate_response
from utils.helper import math_keyboard, render_latex
from utils.plotting import plot_function
from utils.prompting import prompt_SQ, prompt_StepByStep


def math_input_page():


    st.write("""
    Welcome to the Advanced Math Problem Solver! Here's how to use this app:
    1. Choose between 'Text Input' or 'LaTeX Input' tabs.
    2. Use the Math Keyboard to easily input mathematical symbols.
    3. Type your math problem or function in the input field.
    4. Click 'Solve' to get the solution or 'Plot Function' to visualize it.
    5. You can view your problem history and adjust settings in the sidebar.
    """)
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

    solve_col, plot_col, st_by_st = st.columns(3)
    with solve_col:
        solve_button = st.button("Solve", help="Click to solve the problem", use_container_width=True)
    with plot_col:
        plot_button = st.button("Plot Function", help="Click to plot the function", use_container_width=True)
    with st_by_st:
        st_by_st = st.button("Solve Step by step", help="Click to step by step with explanation", use_container_width=True)

    input_to_solve = math_input if tab1 else latex_input
    if input_to_solve:
        if solve_button:
            with st.spinner("Solving the problem..."):
                solution = prompt_SQ(input_to_solve)
                fin_response = generate_response(solution)
                st.subheader("Solution:")
                st.write(fin_response)

        
                # Offer step-by-step explanation
        if st.button("Show step-by-step explanation"):
            sp_by_sp = prompt_StepByStep(input_to_solve)
            explanation = generate_response(sp_by_sp)
            st.write(explanation)
    else:
        st.warning("Please enter a Math problem Above.")

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


def main():
    st.set_page_config(page_title="Advanced Math Problem Solver", page_icon="🧮", layout="wide")

    st.markdown(
        """
        <style>
        .title {
            font-size: 30px;
            font-family: 'Dancing Script', cursive;
            font-weight: lighter;
            color: #333;  /* Optional: Change color */
            text-align: center;
            margin-top: 0px;
        }
        </style>
        """, unsafe_allow_html=True)
    
    st.markdown('<div class="title">Solve Your Maths Problem</div>', unsafe_allow_html=True)
    st.divider()
    st.write('Choose Your Choice 🪧:')
    col1, col2, col3 = st.columns(3)
    with col1:
        st.page_link('app.py', label='Back To Home', icon="🏠")
    with col2:
        st.page_link('pages/Document Solver.py', label='Document Solver', icon="🕒")
    with col3:
        st.page_link('pages/Math Sketchboard.py', label='Math Sketchboard', icon="⬜")

    st.divider()
    
    math_input_page()

    # Sidebar for settings and info
    with st.sidebar:
        
        st.subheader("About")
        st.info(
            "This app uses advanced AI to solve and explain mathematical problems. It can handle a wide range of topics including algebra, calculus, and more.")

        
if __name__ == "__main__":
    main()