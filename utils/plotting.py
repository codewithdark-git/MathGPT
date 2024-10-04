import matplotlib.pyplot as plt
import sympy as sp
import numpy as np
import streamlit as st


def plot_function(func_str, x_range=(-10, 10)):
    try:
        # Define symbols for the equation
        x, y = sp.symbols('x y')

        # Split and parse the equation based on the '=' sign
        if '=' in func_str:
            left, right = func_str.split('=')
            eq = sp.Eq(sp.sympify(left), sp.sympify(right))
        else:
            # If there's no equal sign, assume the function equals 0
            eq = sp.Eq(sp.sympify(func_str), 0)

        # Solve for y if it's present in the equation
        if y in eq.free_symbols:
            solutions = sp.solve(eq, y)
        else:
            # If y is not present, solve for x
            solutions = sp.solve(eq, x)

        # Create x values for plotting
        x_vals = np.linspace(x_range[0], x_range[1], 1000)

        # Prepare plot
        fig, ax = plt.subplots(figsize=(10, 6))

        # Plot all possible solutions for y or x
        for solution in solutions:
            f = sp.lambdify(x, solution, "numpy")  # Lambdify to evaluate the function

            # Try generating y-values, handle constants properly
            try:
                y_vals = f(x_vals)  # Evaluate function
            except TypeError:
                # If the solution is a constant, repeat it for all x_vals
                y_vals = np.full_like(x_vals, float(solution))

            # Plot the result
            ax.plot(x_vals, y_vals, label=f'Solution: {sp.pretty(solution)}')

        # Add title and labels
        ax.set_title(f"Plot of {func_str}")
        ax.set_xlabel('x')
        ax.set_ylabel('y')
        ax.grid(True)

        # Add x and y axis lines for better visibility
        ax.axhline(y=0, color='k', linestyle='-', linewidth=0.5)
        ax.axvline(x=0, color='k', linestyle='-', linewidth=0.5)
        ax.legend()

        return fig

    except sp.SympifyError as e:
        st.error(f"Unable to parse the function: {func_str}. Error: {str(e)}")
    except ValueError as e:
        st.error(f"Error in plotting the equation: {str(e)}")
    except Exception as e:
        st.error(f"An unexpected error occurred: {str(e)}")

    return None
