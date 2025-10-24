
import openai
import os
from dotenv import load_dotenv

load_dotenv()

OPENAI_API_KEY = os.getenv("OPENAI_API_KEY")
client = openai.OpenAI(api_key=OPENAI_API_KEY)

def generate_flashcards(text):
    """
    Uses OpenAI API to generate flashcards from input text.
    Returns a list of dicts: [{"question": ..., "answer": ...}, ...]
    """
    prompt = (
        "Generate flashcards from the following text. "
        "Return a JSON list of objects with 'question' and 'answer' keys.\nText:\n" + text
    )
    try:
        response = client.chat.completions.create(
            model="gpt-3.5-turbo",
            messages=[{"role": "user", "content": prompt}],
            max_tokens=512,
            temperature=0.7
        )
        import json
        # Extract JSON from response
        content = response.choices[0].message.content
        flashcards = json.loads(content)
        return flashcards
    except Exception as e:
        return [{"question": "Error generating flashcards", "answer": str(e)}]
