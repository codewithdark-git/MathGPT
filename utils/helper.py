import requests
import os
from PIL import Image
import pytesseract
import g4f
from g4f.client import Client
from langchain.document_loaders import PyPDFLoader
from langchain.text_splitter import CharacterTextSplitter
from langchain.embeddings import HuggingFaceEmbeddings
from langchain.vectorstores import FAISS
from langchain.chains import RetrievalQA
from langchain.llms import HuggingFaceHub
# from dotenv import load_env

# load_env()


# Ensure you've set up your Hugging Face API token in your environment variables
HuggingFace = os.environ["HuggingFace"]

def solve_math_problem(problem):
    # Placeholder for O1 model integration
    try:
        client = Client
        response = client.chat.completions.create(
            model=g4f.models.gpt_4o,
            messages=[{'role': 'user', 'content': problem}]
        )
        response = response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

def process_whiteboard_image(image):
    # Convert the image to grayscale
    gray_image = Image.fromarray(image).convert('L')
    
    # Use pytesseract to do OCR on the image
    text = pytesseract.image_to_string(gray_image, config='--psm 6')
    
    # Clean up the text (remove newlines, extra spaces, etc.)
    cleaned_text = ' '.join(text.split())
    
    return cleaned_text

def process_uploaded_file(file):
    if file.type == "application/pdf":
        loader = PyPDFLoader(file)
        pages = loader.load_and_split()
    elif file.type == "text/plain":
        text = file.read().decode("utf-8")
        text_splitter = CharacterTextSplitter(chunk_size=1000, chunk_overlap=0)
        pages = text_splitter.split_text(text)
    else:
        raise ValueError("Unsupported file type")

    # Create embeddings
    embeddings = HuggingFaceEmbeddings()
    vectorstore = FAISS.from_documents(pages, embeddings)
    
    return vectorstore

def query_document(vectorstore, question):
    llm = HuggingFaceHub(repo_id="google/flan-t5-xxl", model_kwargs={"temperature":0.5, "max_length":512})
    qa = RetrievalQA.from_chain_type(llm=llm, chain_type="stuff", retriever=vectorstore.as_retriever())
    return qa.run(question)

# Math symbols for the advanced keyboard
MATH_SYMBOLS = [
    '√', 'π', '∑', '∫', '∂', '∞', '±', '≠', '≤', '≥',
    '∈', '∉', '∩', '∪', '⊂', '⊃', '⊄', '⊅', '∀', '∃',
    '→', '←', '↔', '⇒', '⇐', '⇔', '∧', '∨', '¬', '⊕',
    'sin', 'cos', 'tan', 'log', 'ln', 'exp', 'lim', 'sup', 'inf', 'max'
]