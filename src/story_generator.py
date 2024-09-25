from dotenv import load_dotenv
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_KEY"])

prompt = """Write for me a funny story less than 150 words. Be creative as much as possible."""


def generate_script():

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt, generation_config=genai.GenerationConfig(
        temperature=2,
    ))

    return response.text
