import streamlit as st
import numpy as np
from utils.helper import (
    solve_math_problem, process_whiteboard_image, 
    process_uploaded_file, query_document, MATH_SYMBOLS
)

def main():
    st.title("Advanced Math Problem Solver")

    # Sidebar for navigation
    page = st.sidebar.selectbox("Choose a feature", ["Whiteboard", "Math Input", "File Upload & Chat"])

    if page == "Whiteboard":
        whiteboard_page()
    elif page == "Math Input":
        math_input_page()
    elif page == "File Upload & Chat":
        file_upload_and_chat_page()

def whiteboard_page():
    st.header("Whiteboard")
    
    # Use Streamlit's drawing component
    canvas_result = st.empty()
    if st.button("Solve from Whiteboard"):
        if canvas_result.image:
            # Process the whiteboard image
            problem = process_whiteboard_image(canvas_result.image)
            st.write("Detected problem:", problem)
            
            # Solve the problem
            solution = solve_math_problem(problem)
            st.write("Solution:", solution)
        else:
            st.write("Please draw something on the whiteboard first.")

def math_input_page():
    st.header("Math Input")
    
    # Advanced Math Keyboard
    st.subheader("Advanced Math Keyboard")
    cols = st.columns(4)
    for i, symbol in enumerate(MATH_SYMBOLS):
        if cols[i % 4].button(symbol):
            st.session_state.math_input = st.session_state.get('math_input', '') + symbol

    math_input = st.text_input("Enter your math problem:", value=st.session_state.get('math_input', ''))
    st.session_state.math_input = math_input

    if st.button("Solve"):
        solution = solve_math_problem(math_input)
        st.write("Solution:", solution)

def file_upload_and_chat_page():
    st.header("File Upload & Chat")
    uploaded_file = st.file_uploader("Choose a file", type=["pdf", "txt"])
    
    if uploaded_file is not None:
        # Process the uploaded file
        with st.spinner("Processing file..."):
            vectorstore = process_uploaded_file(uploaded_file)
        st.success("File uploaded and processed successfully!")

        # Chat interface
        st.subheader("Chat with your document")
        
        if 'chat_history' not in st.session_state:
            st.session_state.chat_history = []

        for message in st.session_state.chat_history:
            st.write(f"{'You' if message['is_user'] else 'AI'}: {message['text']}")

        user_question = st.text_input("Ask a question about the uploaded document:")
        if st.button("Ask"):
            with st.spinner("Thinking..."):
                answer = query_document(vectorstore, user_question)
            st.session_state.chat_history.append({"text": user_question, "is_user": True})
            st.session_state.chat_history.append({"text": answer, "is_user": False})
            st.experimental_rerun()

if __name__ == "__main__":
    main()