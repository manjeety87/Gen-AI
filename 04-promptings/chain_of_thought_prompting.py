# Chain-of-thought prompting - This is a technique where we provide the model with a series 
# of intermediate reasoning steps that lead to the final answer. This helps the model to 
# reason through complex problems and generate more accurate responses.

from dotenv import load_dotenv
from openai import OpenAI
from google import genai
import time
import json
from google.genai import errors

load_dotenv()

client = OpenAI()
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


# response = client.chat.completions.create(
#     model="gpt-4.1-mini", 
#     response_format={"type":"json_object"},
#     messages=[
#         {"role": "system", "content": SYSTEM_PROMPT},
#         {"role": "user", "content": "What is 2 + 3 / 3 to the power 2"},
#         {"role": "assistant", "content": json.dumps({"step": "analyse", "content": "The user wants to calculate the expression 2 + 3 / 3 to the power 2. This involves addition, division, and exponentiation operations."} )},
#         {"role": "assistant", "content": json.dumps({"step": "think", "content": "According to the order of operations (PEMDAS/BODMAS), I need to solve the exponentiation first, then division, and finally addition."})},
#         {"role": "assistant", "content": json.dumps({"step": "think again", "content": "The expression can be interpreted as 2 + (3 / 3^2). I should calculate 3^2 first which is 9, then divide 3 by 9, and finally add 2 to the result."} )},
#         {"role": "assistant", "content": json.dumps({"step": "think several times", "content": "Calculating 3^2 = 9, then 3 / 9 = 1/3 or approximately 0.3333, and adding 2 gives 2 + 0.3333 = 2.3333. Therefore, the value of the expression is approximately 2.3333."}  )},
#         {"role": "assistant", "content": json.dumps({"step": "result", "content": "The value of 2 + 3 / 3^2 is 2 + 3/9 = 2 + 1/3 = 2.3333 (approximately)."})},
#         {"role": "assistant", "content": json.dumps({"step": "validate", "content": "The calculations follow the order of operations correctly. 3^2 is 9, 3 divided by 9 is 1/3, and adding 2 gives 2.3333. The answer is valid."})},
#         {"role": "assistant", "content": json.dumps({"step": "result", "content": "2 + 3 / 3^2 = 2 + 3/9 = 2 + 1/3 = 2.3333 (approximately) is the correct result."})},
        
#         ] 
# )

# print("\n\n🤖",response.choices[0].message.content,"\n\n")


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


def get_openai_response(messages):
    response = client.chat.completions.create(
        model="gpt-4.1-mini",
        response_format={"type": "json_object"},
        messages=messages
    )
    return response.choices[0].message.content

def get_gemini_response(messages):
    response = gemeniClient.models.generate_content(
        model='gemini-2.5-flash',
        contents=json.dumps(messages),
    )
    return response.text

while True:
    response =get_openai_response(messages)

    # Add assistant response back to messages
    messages.append({"role": "assistant", "content": response})

    parsed_response = json.loads(response)

    step = parsed_response.get("step")
    answer = parsed_response.get("content")
    
    if step == "think" or step == "think again" or step == "think several times":
        #Make the GEMINI API call or CLAUDE and append the result as validate.
        try:
            geminiRes = get_gemini_response(messages)
            messages.append({"role": "assistant", "content": geminiRes})
            continue
        except errors.ClientError as e:
            print("API limit error. Wait and try again.")
            time.sleep(5)

    if step != "result":
        print(f"\n🧠 {step}: {answer}\n")

        # Tell model to continue next step
        messages.append({"role": "user", "content": "Continue with the next step."})
        continue

    print(f"\n🤖 Final Answer: {answer}\n")
    break

# messages = [
#     {"role": "system", "content": SYSTEM_PROMPT},
# ]


# query = input(">: ")
# messages.append({"role": "user", "content": query})

# while True:
#     response = client.chat.completions.create(
#         model="gpt-4.1",
#         response_format={"type":"json_object"},
#         messages=messages
#     )
    
#     messages.append({"role": "assistant", "content": json.dumps(response.choices[0].message.content)})
#     parsed_response = json.loads(response.choices[0].message.content)
    
#     # if parsed_response.get("step") != "result":
#     #     print("\n\n🧠 : ",parsed_response,"\n")
#     #     messages.append({"role": "user", "content": query})
#     # else:
#     #     print("\n\n🤖 : ",parsed_response,"\n")
#     #     break
    
#     if parsed_response.get("step") != "result":
#         print("\n🧠 ... : ",parsed_response.get("content"),"\n")
#         continue
    
#     print("\n🤖 : ",parsed_response.get("content"),"\n")
#     break