########################################
# LLM Prompt Controller for Math Solutions
########################################

# Function to generate a prompt from extracted text on the whiteboard
def prompt_WB(extracted_text):
    """
    Generate a prompt from the mathematical equation or problem extracted from the whiteboard.

    Parameters:
    extracted_text (str): The mathematical equation or problem extracted from the whiteboard.

    Returns:
    str: The formatted prompt to be sent to the LLM for solving.
    """
    prompt = f"""
    As a mathematical expert, analyze and solve the following handwritten mathematical equation or problem captured from a digital whiteboard:

    {extracted_text}

    Provide a step-by-step solution, focusing solely on mathematical operations and reasoning. Include:
    1. Any necessary clarifications or interpretations of the handwritten problem
    2. Each mathematical step taken to solve the problem
    3. The final, precise answer

    Avoid verbose explanations. Use mathematical notation where appropriate. Ensure all steps are logically connected and lead to the correct solution.
    """
    return prompt

# Function to generate a prompt from text extracted from file/imag
def prompt_FP(user_input, extracted_text):
    """
    Generate a prompt from the mathematical equation or problem based on user input and the extracted text.

    Parameters:
    user_input (str): The user's desired action for the mathematical problem (e.g., Solve, Analyze, Get Hints).
    extracted_text (str): The mathematical equation or problem extracted from a file or image.

    Returns:
    str: The formatted prompt to be sent to the LLM for solving or analysis based on user input, without using LaTeX format.
    """
    
    prompt = f"""
    As a mathematical expert, based on the user's request to "{user_input}" the following mathematical equation or problem extracted from an uploaded document:

    {extracted_text}

    Please provide the response **without using LaTeX formatting**.

    If the request is to **Solve**, provide a concise, step-by-step solution that includes:
    1. Interpretation of the problem (if needed)
    2. Each mathematical step, using appropriate notation (but not in LaTeX)
    3. The final, precise answer

    If the request is to **Analyze**, provide a detailed breakdown of the problem, including key concepts, mathematical operations, and reasoning, without necessarily providing a final answer.

    If the request is for **Hints**, provide a few guiding steps that could help the user solve the problem on their own, but do not reveal the full solution.

    Ensure all steps are clear, accurate, and logically aligned with the requested action. Avoid using LaTeX or unnecessary verbosity.
    """
    
    return prompt



# Function to generate a prompt from user input in a text form
def prompt_SQ(extracted_text):
    """
    Generate a prompt from the mathematical equation or problem entered by the user.

    Parameters:
    extracted_text (str): The mathematical equation or problem directly entered by the user.

    Returns:
    str: The formatted prompt to be sent to the LLM for solving.
    """
    prompt = f"""
    As a mathematical expert, solve the following problem entered by a user:

    {extracted_text}

    Provide a precise, step-by-step solution that includes:
    1. Clarification of the problem (if necessary)
    2. Each mathematical step, using appropriate notation and symbols
    3. The final, accurate answer

    Focus solely on mathematical operations and reasoning. Ensure each step is clear, correct, and leads logically to the solution. Avoid unnecessary explanations and concentrate on the mathematical process.
    """
    return prompt


# Function to generate a detailed, step-by-step explanation for any math problem
def prompt_StepByStep(extracted_text):
    """
    Generate a prompt for providing a detailed, step-by-step breakdown of a solution.

    Parameters:
    extracted_text (str): The mathematical equation or problem that requires a detailed step-by-step solution.

    Returns:
    str: The formatted prompt to be sent to the LLM for a detailed breakdown of the solution.
    """
    prompt = f"""
    As a mathematical expert, provide a comprehensive, step-by-step solution to the following problem:

    {extracted_text}

    Your explanation should:
    1. Begin with a clear interpretation of the problem
    2. Break down the solution into logical, numbered steps
    3. Use precise mathematical language and notation for each step
    4. Explain the reasoning behind each step, including any theorems or principles applied
    5. Clearly show how each step leads to the next
    6. Conclude with the final, accurate answer

    Aim for clarity and completeness. While the explanation should be detailed, ensure it remains focused on the mathematical concepts and operations involved. Use examples or analogies only if they significantly enhance understanding of a complex step.
    """
    return prompt