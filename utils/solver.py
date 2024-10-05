from sympy import sympify

def solve_math_expression(expression):
    try:
        result = sympify(expression)
        return result
    except Exception as e:
        return f"Error: {str(e)}"
