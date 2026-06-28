from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# text = "dog chases cat"
text = "cat chases dog"

response = client.embeddings.create(
    model="text-embedding-3-small",
    # model="gpt-5.5",
    input=text
)

print("Output text is :",response)
print("Length of embeddings :",len(response.data[0].embedding))
# print("Embedding vector is :", response.data[0].embedding)