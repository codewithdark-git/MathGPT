import streamlit as st
import sympy as sp
import spacy

# Load the NLP model
nlp = spacy.load('en_core_web_sm')


# Function to parse and solve math problems
def extract_math_expressions(problem):
    doc = nlp(problem)
    expressions = []
    for sent in doc.sents:
        tokens = [token.text for token in sent if token.like_num or token.pos_ in {'NOUN', 'VERB', 'NUM', 'SYM'}]
        if tokens:
            expressions.append(' '.join(tokens))
    return expressions


def solve_math_problem(problem):
    try:
        expressions = extract_math_expressions(problem)
        if not expressions:
            return None, "No valid mathematical expression found."

        results = []
        for expr in expressions:
            sympy_expr = sp.sympify(expr)
            solution = sp.simplify(sympy_expr)
            results.append((sympy_expr, solution))

        return results, None
    except Exception as e:
        return None, str(e)


# Streamlit app setup
def main():
    st.title("Advanced Math Problem Solver Bot")

    st.markdown("## Enter your math problem")
    math_problem = st.text_area("Describe your math problem:", height=150)

    if st.button("Solve"):
        if math_problem.strip():
            solutions, error = solve_math_problem(math_problem)
            st.markdown("### Solution")
            if solutions:
                for i, (expr, solution) in enumerate(solutions):
                    st.write(f"**Expression {i + 1}:** {expr}")
                    st.write(f"**Simplified Solution {i + 1}:** {solution}")
            else:
                st.error(f"Error: {error}")
        else:
            st.error("Please enter a math problem to solve")

    st.markdown("## How to Use")
    st.write("Describe your math problem in the text area above and click on the 'Solve' button.")

    st.markdown("## About")
    st.write(
        "This advanced bot uses NLP and SymPy to solve mathematical problems. It can handle basic arithmetic, algebra, and calculus problems with natural language input.")

    st.markdown("## Footer")
    st.write("Created by [Your Name]")


if __name__ == "__main__":
    main()
