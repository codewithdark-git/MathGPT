import streamlit as st

def main():

    st.markdown(
        """
        <style>
        .title {
            font-size: 50px;
            font-weight: bold;
            color: #4F8BF9;  /* Optional: Change color */
            text-align: center;
            margin-bottom: 0px;
        }
        .subtitle {
            font-size: 30px;
            font-weight: lighter;
            color: #333;  /* Optional: Change color */
            text-align: center;
            margin-top: 0px;
        }

        .developer {
        font-size: 15px;
        font-weight: lighter;
        color: #777;
        text-align: center;
        position: fixed;
        bottom: 10px;
        width: 100%;
        }
        .developer a {
            color: #4F8BF9;
            text-decoration: none;
            font-weight: bold;
        }
        .developer a:hover {
            text-decoration: underline;
        }
        .emoji {
            font-size: 20px;
            margin-left: 5px;
        }
        </style>
        """, unsafe_allow_html=True
    )

    # Add the title and subtitle
    st.markdown('<div class="title">MathGPT</div>', unsafe_allow_html=True)
    st.markdown('<div class="subtitle">Your Advanced Math Problem Solver</div>', unsafe_allow_html=True)

    st.divider()
    
    st.write('Choose Your Choice 🪧:')
    col1, col2, col3 = st.columns(3)
    with col1:
        if st.button('Solve Question With LLM'):
            st.switch_page("pages/Solve Question.py")
    with col2:
        if st.button('File Question'):
            st.switch_page("pages/File Process.py")
    with col3:
        if st.button('White Board'):
            st.switch_page("pages/White Board.py")

    # Overview description
    st.write("""
    **MathGPT** is a web application built with Streamlit that allows users to input mathematical problems and receive solutions. The app supports both text and LaTeX input, making it versatile for various mathematical expressions. Users can also visualize functions and access a history of their solved problems.
    """)

    # Features section
    st.subheader("Features")
    st.write("""
    - **Upload File**: Upload images or PDF files containing math problems.
    - **Select OR Draw**: Draw a box around the text or equation you want to OCR.
    - **Input Methods**: Choose between text input and LaTeX input for entering mathematical problems.
    - **Math Keyboard**: A user-friendly math keyboard for easy symbol insertion.
    - **Problem Solving**: Click "Solve" to get solutions for your math problems.
    - **Function Plotting**: Visualize mathematical functions with the "Plot Function" feature.
    - **History Tracking**: Keep track of previously solved problems.
    - **Step-by-Step Explanations**: Get detailed explanations for solutions.
    """)

    # Usage instructions
    st.subheader("Usage")
    st.write("""
    1. **Open the app**: After running the application, it will open in your default web browser.
    2. **Upload File**: After the model loads, upload an image or a PDF.
    3. **Select OR Draw**: Draw a box around the equation or text you want to OCR by clicking and dragging.
    4. **Input your problem**: Use the "Text Input" or "LaTeX Input" tabs to enter your mathematical problem.
    5. **Use the Math Keyboard**: Click on symbols to insert them into your input.
    6. **Solve or Plot**: Click "Solve" to get the solution or "Plot Function" to visualize the function.
    7. **View History**: Access the "Problem History" section to see previously solved problems.
    """)

    # Feedback section
    st.subheader("Feedback")
    st.write("""
    We appreciate your feedback! Use the feedback section in the sidebar to share your thoughts or report issues.
    """)

    # License
    st.subheader("License")
    st.write("""
    This project is licensed under the MIT License. See the LICENSE file for details.
    """)

    # Acknowledgments
    st.subheader("Acknowledgments")
    st.write("""
    - **Streamlit** for the framework.
    - **latex2mathml** for LaTeX rendering.
    - **Pandas** for data manipulation.
    - **Pillow** for image processing.
    - **Texify** for image and PDF Processing.
    """)

    st.markdown(
    """
    <div class="developer">
        Developed by <a href="https://github.com/codewithdark-git" target="_blank">Codewithdark</a> & 
        <a href="https://github.com/aisha-iftikhar" target="_blank">Aisha Iftikhar</a>
        <span class="emoji">🚀</span>
    </div>
    """, unsafe_allow_html=True
)

if __name__ == '__main__':
    main()
