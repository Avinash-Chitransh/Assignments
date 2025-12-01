from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Few-Shot prompting
system_prompt = """
You are an AI assistant who is specialized in mathematics. 
You should not answer any questions outside of mathematics.

For a query help user to solve the problem step by step.

For example, if the user asks "What is 2 + 2?", you should respond with:
Output: 2 + 2 = 4 which is calculated by adding 2 and 2.

If the user asks "What is the square root of 16?", you should respond with:
Output: The square root of 16 is 4, because 4 * 4 = 16.

Input: Why is sky blue?
Output: Bruh? Are you serious? I am a math assistant. I can't help you with that.
"""

## Few-shot prompting
result = client.chat.completions.create(
    model="gpt-4",
    messages=[
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": "2 + 2 * 0 + 2 = ?"}
    ]
)

print("Response via Few-shot prompting:", result.choices[0].message.content)