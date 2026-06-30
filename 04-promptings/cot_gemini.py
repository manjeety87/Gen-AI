from dotenv import load_dotenv
from google import genai
import time
import json
from google.genai import errors

load_dotenv()

gemeniClient = genai.Client()


# Chain of thought - This model is encouraged to think step by step and provide reasoning before giving the final answer. This can help in solving complex problems and generating more accurate responses.

SYSTEM_PROMPT = """You are an helpful AI assistant who is specialized in solving user queries.
For the given user input, analyse the input and break down the problem step by step.


The steps are you get a user input, then you analyze, you think, you think again and think several times before you give the final answer.

Follow the steps that is "analyse", "think", "think again", "think several times" and then "result" with "validation".

Rules:
1. Follow the strict JSON format for the output.
2. Always perform one step at a time and wait for the next input.
3. Carefully analyze the user input and provide reasoning before giving the final answer.
4. Return raw JSON only. Do not use markdown. Do not wrap output in ```json or ```.

Output format:
{{"step": "string", "content": "string"}}

Example:
Input: What is the sum of 2 and 3?
Output: {{"step": "analyse", "content": "Alright! The user is interested in maths Arithmatic query, and he wants to know the sum of 2 and 3."}}
Output: {{"step": "think", "content": "To perform this sum we need to do addition, I must add the two numbers together."}}
Output: {{"step": "output", "content": "5"}}
Output: {{"step": "validate", "content": "Looks like 5 is the correct answer for 2 + 3"}}
Output: {{"step": "result", "content": "2 + 3 = 5, and this is calculated by adding the two numbers together."}}

Example:
    Input: What is 2 + 2 * 5 / 3
    Output: {{ "step": "analyse", "content": "Alight! The user is interest in maths query and he is asking a basic arthematic operations" }}
    Output: {{ "step": "think", "content": "To perform this addition, I must use BODMAS rule" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS is the right approach here" }}
    Output: {{ "step": "think", "content": "First I need to solve division that is 5 / 3 which gives 1.66666666667" }}
    Output: {{ "step": "validate", "content": "Correct, using BODMAS the division must be performed" }}
    Output: {{ "step": "think", "content": "Now as I have already solved 5 / 3 now the equation looks lik 2 + 2 * 1.6666666666667" }}
    Output: {{ "step": "validate", "content": "Yes, The new equation is absolutely correct" }}
    Output: {{ "step": "validate", "think": "The equation now is 2 + 3.33333333333" }}
    and so on.....

"""

# SYSTEM_PROMPT = """
# You are a helpful AI assistant.

# For the given user input, solve the problem using simple structured steps.

# You must follow this step order:
# 1. analyse
# 2. plan
# 3. think
# 4. think again
# 5. solve
# 6. validate
# 7. result

# Rules:
# 1. Always return only one JSON object.
# 2. Follow this JSON format only:
#    {"step": "string", "content": "string"}
# 3. Keep reasoning short and easy to understand.
# 4. Do not give long hidden chain-of-thought.
# 5. When the final answer is ready, use step as "result".
# """

messages = [
    {"role": "system", "content": SYSTEM_PROMPT}
]

query = input("Ask something: ")
messages.append({"role": "user", "content": query})

# response = gemeniClient.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=json.dumps(messages),
#             # config={"thinking_level": "high"},
#             )
  
# content = response.text
# print("Raw content:", content)  
    
# content = response.text
# print("Content:", content)
# parsed_response = json.loads(content)

# step = parsed_response.get("step")
# answer = parsed_response.get("content")
# print("Step:", step)
# print("Answer:", answer)

# while True:
#     response = gemeniClient.models.generate_content(
#             model='gemini-2.5-flash',
#             contents=json.dumps(messages),
#             )
    
#     content = response.text
    
#     messages.append({"role": "assistant", "content": content})
    
#     parsed_response = json.loads(content)
#     step = parsed_response.get("step")
#     answer = parsed_response.get("content")
    
#     if step != "result":
#         print(f"\n🧠 {step}: {answer}\n")

#         # Tell model to continue next step
#         messages.append({"role": "user", "content": "Continue with the next step."})
#         continue

#     print(f"\n🤖 Final Answer: {answer}\n")
#     break

while True:
    try:
        response = gemeniClient.models.generate_content(
            model="gemini-2.5-flash",
            contents=json.dumps(messages),
        )

        content = response.text.strip()
        print("Raw content:", response.text)  # Print the raw content for debugging
        messages.append({"role": "assistant", "content": response.text})

        parsed_response = json.loads(response.text)
        step = parsed_response.get("step")
        answer = parsed_response.get("content")

        if step != "result":
            print(f"\n🧠 {step}: {answer}\n")
            messages.append({"role": "user", "content": "Continue with the next step."})
            time.sleep(2)
            continue

        print(f"\n🤖 Final Answer: {answer}\n")
        break

    except errors.ClientError as e:
        print("API limit error. Wait and try again.")
        time.sleep(5)