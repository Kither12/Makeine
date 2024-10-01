from datetime import datetime
from dotenv import load_dotenv
import re
import json
import google.generativeai as genai
import os

load_dotenv()
genai.configure(api_key=os.environ["GEMINI_KEY"])

prompt = """# Instructions
Given the following video script and timed captions, extract the prompt that use for background videos. Each prompt for each timestamp must be independence and in term of context. The prompt for each timestamp must be diffrent from each other. The prompts must not contain any names or nicknames and the subject such as "he", "she", "they", "it". The output should be in JSON format, like this: [[[t1, t2], "prompt1"], [[t2, t3], "prompt2"], ...]
"""

main_keyword = """# Instructions
Given the following video script, extract five main keywords from it. The keywords should not contains any names or nicknames. The output should be in this format: keyword1, keyword2, keyword3, keyword4, keyword5.
"""


def generateMainKeyWords(script):
    user_content = """Script: {}""".format(script)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(main_keyword + " " + user_content, generation_config=genai.GenerationConfig(
        temperature=2,
    ))

    return response.text


def getVideoPromptTimed(script, captions_timed):
    end = captions_timed[-1][0][1]
    try:

        out = [[[0, 0], ""]]
        while out[-1][0][1] != end:
            content = call_Gemini(script, captions_timed)
            content = content.replace("```json", "").replace("```", "")
            print(content)
            out = json.loads(content)
        return out
    except Exception as e:
        print("error in response", e)

    return None


def call_Gemini(script, captions_timed):
    user_content = """Script: {}
Timed Captions:{}
""".format(script, "".join(map(str, captions_timed)))
    print("Content", user_content)

    model = genai.GenerativeModel("gemini-1.5-flash")
    response = model.generate_content(prompt + " " + user_content, generation_config=genai.GenerationConfig(
        temperature=2,
    ))

    text = response.text
    print("Prompt time: ", text)
    return text
