# Advanced Math Problem Solver

## Overview

The **Advanced Math Problem Solver** is a web application built with Streamlit that allows users to input mathematical problems and receive solutions. The app supports both text and LaTeX input, making it versatile for various mathematical expressions. Users can also visualize functions and access a history of their solved problems.

## Features

- **Upload File**: Upload images or PDF files.
- **Select OR Draw**: Draw a box around the text or equation you want to OCR.
- **Input Methods**: Choose between text input and LaTeX input for entering mathematical problems.
- **Math Keyboard**: A user-friendly math keyboard for easy symbol insertion.
- **Problem Solving**: Click "Solve" to get solutions for your math problems.
- **Function Plotting**: Visualize mathematical functions with the "Plot Function" feature.
- **History Tracking**: Keep track of previously solved problems.
- **Step-by-Step Explanations**: Get detailed explanations for solutions.

## Installation

To run this application locally, follow these steps:

1. **Clone the repository**:
   ```bash
   git clone https://github.com/codewithdark-git/MathGPT.git
   cd MathGPT
   ```

2. **Create a virtual environment** (optional but recommended):
   ```bash
   python -m venv venv
   venv\Scripts\activate
   ```

3. **Install the required packages**:
   ```bash
   pip install -r requirements.txt
   ```

4. **Run the application**:
   ```bash
   streamlit run app.py
   ```

## Usage

1. **Open the app**: After running the application, it will open in your default web browser.
2. **Upload File**: After the model loads, upload an image or a PDF.
3. **Select OR Draw**: Draw a box around the equation or text you want to OCR by clicking and dragging.
4. **Input your problem**: Use the "Text Input" or "LaTeX Input" tabs to enter your mathematical problem.
5. **Use the Math Keyboard**: Click on symbols to insert them into your input.
6. **Solve or Plot**: Click "Solve" to get the solution or "Plot Function" to visualize the function.
7. **View History**: Access the "Problem History" section to see previously solved problems.

## Feedback

We appreciate your feedback! Use the feedback section in the sidebar to share your thoughts or report issues.

## License

This project is licensed under the MIT License. See the LICENSE file for details.

## Acknowledgments

- [Streamlit](https://streamlit.io/) for the framework.
- [latex2mathml](https://github.com/latex2mathml/latex2mathml) for LaTeX rendering.
- [Pandas](https://pandas.pydata.org/) for data manipulation.
- [Pillow](https://python-pillow.org/) for image processing.
- [Texify](https://github.com/VikParuchuri/texify.git) for image and PDF Processing
