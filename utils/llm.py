import g4f
from g4f.client import Client


def generate_response(problem: str) -> str:
    try:
        client = Client()
        response = client.chat.completions.create(
            model=g4f.models.gpt_4,
            messages=[{'role': 'user', 'content': f"Solve this math problem step by step: {problem}"}]
        )
        return response.choices[0].message.content
    except Exception as e:
        return f"Error: {str(e)}"

