from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

response = client.chat.completions.create(
    model="gpt-4.1-mini", #we could use any model here, but this is the most cost effective for a simple hello world
    # messages=[{"role": "user", "content": "Hello world"}]
    # messages=[{"role": "user", "content": "What is the time right now ?"}]
    # messages=[{"role": "user", "content": "What is weather right now ?"}] 
    # messages=[{"role": "user", "content": "Hey, My name is Mann"}]#All these are stateless. This wont be able to store the name as the state is not maintained.
    messages=[{"role": "user", "content": "Hey, My name is Mann"},
              {"role": "assistant", "content": "Hii, Mann! How can I assist you today?"},
              {"role": "user", "content": "Can you remember my name ?"},
              {"role": "assistant", "content": "I can remember your name during this conversation, Mann! However, I won’t be able to recall it once our chat ends. How can I help you today?"},
              {"role": "user", "content": "How are you doing ?"},
              {"role": "assistant", "content": "I'm doing great, thanks for asking, Mann! How about you?"}] 
)

print("Response is :",response.choices[0].message.content)

#In order to maintain the state we have to add the previous messages in the next request. This is how we can maintain the state of the conversation. So whatever the assistant says, we have to add that in the next request as well. This is how we can maintain the state of the conversation.
# The last request will only be the one which will be sent to the model rest before that all would be cached input. So the model will be able to understand the context of the conversation and will be able to respond accordingly.
# Also we have limited tokens in the request. So we have to be careful about the number of messages we are sending in the request. If we send too many messages, we might exceed the token limit and the model will not be able to respond.
# Suppose we have 500 messages summarize the last 400 messages in 1 message and send this 1 message with 101 message so that it won't forget the context.
# It is not necessary it is one of the way to reduce the number of messages.

# response1 = client.responses.create(
#     model="gpt-4.1-mini",
#     input="What is the weather right now ?"
# )

# print("Response is :", response1.output_text)