from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Zero Shot Prompting
result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "user", "content": "2 + 2 * 0 + 2 = ?"} 
    ]
)

print("Response via Zero-shot prompting:", result.choices[0].message.content)