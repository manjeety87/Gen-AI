## Prompt Formats

Different LLMs different prompt formats use kar sakte hain.

As a developer, hume basic idea hona chahiye ki model ko input kis format mein diya ja raha hai.

## 1. Alpaca Prompt Format

Alpaca style prompt format usually instruction/input/response type structure use karta hai.

Example:

```text
### Instruction:
Explain tokenization in simple words.

### Input:
Hello, I am Mann

### Response:
Tokenization means breaking text into small pieces called tokens.
```

Is type ka format kuch open-source models ya fine-tuning datasets mein dekhne ko mil sakta hai.

## 2. ChatML / Role Based Format

OpenAI style mein hum usually role based messages use karte hain.

Example:

```python
messages=[
    {"role": "system", "content": "You are a helpful assistant."},
    {"role": "user", "content": "Explain tokenization in simple words."}
]
```

Yahan roles important hote hain:

```text
system = model ko behavior/instructions dena
user = user ka actual question
assistant = model ka previous reply
```

As a developer, hum mostly isi type ka format use karte hain jab Chat Completions API use karte hain.

## 3. INST Format

Kuch models instruction format use karte hain.

Example:

```text
[INST] What is an LRU Cache? [/INST]
```

Ye format mostly kuch open-source/instruction-tuned models mein use hota hai.

## Important Note

Majorly jab hum OpenAI API use karte hain, to hume manually Alpaca, INST, ya raw internal prompt format likhne ki zaroorat nahi hoti.

Hum normally simple API format use karte hain.

For Chat Completions API:

```python
messages=[
    {"role": "user", "content": "Hello world"}
]
```

For Responses API:

```python
input="Hello world"
```

Internally model/pipeline required formatting handle kar leta hai.

## Simple Summary

```text
Alpaca Format = Instruction/Input/Response style
ChatML / Role Based Format = system, user, assistant messages
INST Format = [INST] question [/INST]
```

For most OpenAI API projects, we use role based messages or simple input.


# Hello World using OpenAI API

In this lesson, I am learning how to call OpenAI model using Python.

Here I tried two ways:

```text
1. Chat Completions API
2. Responses API
```

## Important Difference

Both APIs can generate text output, but syntax is different.

## 1. Chat Completions API

Chat Completions API mein hum `messages` use karte hain.

```python
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello world"}]
)

print(response.choices[0].message.content)
```

Yahan output nikalne ke liye hum use karte hain:

```python
response.choices[0].message.content
```

## 2. Responses API

Responses API newer and simpler API hai.

Isme hum `input` use karte hain.

```python
response1 = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello world"
)

print(response1.output_text)
```

Yahan output nikalne ke liye hum use karte hain:

```python
response1.output_text
```

## Full Code

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# Chat Completions API
response = client.chat.completions.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello world"}]
)

print("Chat Completions Response is:", response.choices[0].message.content)


# Responses API
response1 = client.responses.create(
    model="gpt-4.1-mini",
    input="Hello world"
)

print("Responses API Response is:", response1.output_text)
```

## Common Mistakes I Faced

### Mistake 1

I used `messages` inside `client.responses.create()`.

```python
client.responses.create(
    model="gpt-4.1-mini",
    messages=[{"role": "user", "content": "Hello world"}]
)
```

This gives error because Responses API does not use `messages`.

Correct way:

```python
client.responses.create(
    model="gpt-4.1-mini",
    input="Hello world"
)
```

### Mistake 2

I used `response.choices[0].message.content` with Responses API.

That is wrong because Responses API does not have `choices`.

Correct way:

```python
response1.output_text
```

## Weather and Time Question

When I asked:

```text
What is the weather right now?
```

Model replied that it does not have real-time data.

This is correct because normal model call does not automatically know live weather or current time.

For real-time weather, time, news, or live data, we need to connect tools or external APIs.

Example:

```text
Weather API
Time API
Web search tool
Function calling
```

## Simple Summary

```text
Chat Completions API:
Uses messages
Output: response.choices[0].message.content

Responses API:
Uses input
Output: response.output_text
```

## Which One Should I Use?

For new projects, Responses API is better because it is newer and simpler.

But Chat Completions API is still useful to understand because many tutorials and old projects use it.

## Final Understanding

In this lesson, I learned how to send a simple prompt to OpenAI model and get response back.

I also learned that model does not automatically know live data like current time or weather.

If we need real-time data, we have to connect external tools or APIs.
