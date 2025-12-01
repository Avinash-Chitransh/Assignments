from dotenv import load_dotenv
from openai import OpenAI
import json

load_dotenv()

client = OpenAI()

system_prompt = """
You are an AI assistant who is expert in breaking down complex problems into simpler steps.

For the given user query, analyze the input and break it down into smaller, manageable steps.
Atleast think 5-6 steps on how to solve the problem before providing the final answer.

The steps are you get get a user input, you analyze the input, you think, you again think for several times and then return the final answer with the appropriate explanations and finally you validate the results before giving the final answer.

Follow the steps in sequence that is "analyze", "think", "output", "validate", and "final_answer".

Rules:
1. Follow the strict JSON output as per the output schema.
2. Always perform one step at a time and wait for the next input
3. Carefully analyze the user query

Ouput Format:
{{step: "string", content: "string"}}

Example:
Input: What is 2 + 2 * 0 + 2?
Output: {{step: "analyze", content: "Alright, the user is interested in mathematical query having the expression that contains addition and multiplication."}}
Output: {{step: "think", content: "Let's break it down step by step."}}
Output: {{step: "think", content: "First, we need to handle the multiplication part of the expression."}}
Output: {{step: "think", content: "The multiplication 2 * 0 equals 0."}}
Output: {{step: "think", content: "Now we can rewrite the expression as 2 + 0 + 2."}}
Output: {{step: "think", content: "Next, we can perform the addition."}}
Output: {{step: "think", content: "2 + 0 equals 2, and then adding the last 2 gives us 4."}}
Output: {{step: "output", content: "So, the final answer is 4."}}
Output: {{step: "validate", content: "Let's double-check: 2 + 2 * 0 + 2 = 2 + 0 + 2 = 4. Everything checks out!"}}
Output: {{step: "final_answer", content: "The final answer is 4."}}
"""

## Chain of thought prompting
messages = [
    {"role": "system", "content": system_prompt}
]

query = input("Enter your query: ")
messages.append({"role": "user", "content": query})

# Initialize the OpenAI client with the system prompt
while True:
    response = client.chat.completions.create(
        model="gpt-4o",
        response_format={"type": "json_object"},
        messages=messages
    )

    parsed_response = json.loads(response.choices[0].message.content)
    messages.append({
        "role": "assistant",
        "content": json.dumps(parsed_response)
    })


    if parsed_response['step'] != "final_answer":
        print(f"🧠: {parsed_response['content']}")
        continue
    print("Final Answer:", parsed_response['content'])
    break

## Few shot prompting
'''
result = client.chat.completions.create(
    model="gpt-4o",
    response_format={"type":"json_object"},
    messages=[
        {"role": "system", "content": system_prompt}, 
        {"role": "user", "content": "What is 3 + 4 * 5 = ?"},
        {"role": "assistant", "content": json.dumps({"step":"analyze", "content": "The user has provided a mathematical expression that involves addition and multiplication: 3 + 4 * 5"})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "Let's break it down step by step according to the order of operations."})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "First, we should handle the multiplication part of the expression 4 * 5."})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "Calculating 4 * 5 gives us 20."})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "Now we can rewrite the expression as 3 + 20."})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "Next, we can perform the addition."})},
        {"role": "assistant", "content": json.dumps({"step":"think", "content": "3 + 20 equals 23."})},
        {"role": "assistant", "content": json.dumps({"step":"output", "content": "So, the final value of the expression 3 + 4 * 5 is 23."})},
        {"role": "assistant", "content": json.dumps({"step":"validate", "content": "Let's double-check: first calculating the multiplication 4 * 5 = 20, then adding 3 gives us 23. Everything checks out!"})},
        {"role": "assistant", "content": json.dumps({"step":"final_answer", "content": "The final answer for the expression 3 + 4 * 5 is 23."})}
    ]
)

print("Response:", result.choices[0].message.content)
'''