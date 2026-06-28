# Vector Embeddings using OpenAI

In previous lesson, humne **Tokenization** padha.

Tokenization mein humne dekha ki text tokens mein convert hota hai.

Ab next step hai:

```text
Text → Vector Embeddings
```

## What are Vector Embeddings?

Vector embeddings ka matlab hota hai text ko numbers ke vector format mein convert karna.

Simple words mein:

> Embedding ek list hoti hai numbers ki, jo text ka meaning represent karti hai.

Example:

```text
cat chases dog
```

Is text ko embedding model ek long vector mein convert karega.

Example:

```text
[0.012, -0.045, 0.087, 0.031, ...]
```

Ye numbers random nahi hote. Ye text ke meaning ko represent karte hain.

## Why Do We Need Embeddings?

AI model normal text ko directly human ki tarah understand nahi karta.

Model numbers ke saath kaam karta hai.

So embeddings ka kaam hota hai text ka meaning numbers mein convert karna.

Simple difference:

```text
Tokenization = text ko tokens mein todna
Embeddings = text ka meaning numbers mein represent karna
```

Embeddings ka use hota hai:

```text
Semantic search
Similarity check
RAG applications
Vector database
Chatbot memory
Recommendation system
```

## Install Required Packages

```bash
pip install openai python-dotenv
```

## Create `.env` File

Project folder ke andar `.env` file create karo.

```text
02 - vector_embeddings
│
├── .env
├── main.py
└── README.md
```

`.env` file ke andar apni OpenAI API key add karo:

```env
OPENAI_API_KEY=your_api_key_here
```

Important:

```text
.env file ko GitHub pe push nahi karna.
```

API key private hoti hai, so `.env` file ko `.gitignore` mein add karna better hai.

## Full Code

```python
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI()

# text = "dog chases cat"
text = "cat chases dog"

response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)

print("Output text is :", response)
print("Length of embeddings :", len(response.data[0].embedding))

# print("Embedding vector is :", response.data[0].embedding)
```

## Code Explanation

First, we load the `.env` file:

```python
load_dotenv()
```

Isse hamari OpenAI API key load hoti hai.

Then we create OpenAI client:

```python
client = OpenAI()
```

Now we give input text:

```python
text = "cat chases dog"
```

Then we create embedding:

```python
response = client.embeddings.create(
    model="text-embedding-3-small",
    input=text
)
```

Yahan hum `text-embedding-3-small` model use kar rahe hain.

Important note:

```python
# model="gpt-5.5"
```

Ye yahan use nahi karna, because GPT model text generation ke liye hota hai.

Embeddings ke liye embedding model use karna hota hai.

## Output

Response ke andar embedding vector aata hai.

Example output short form mein:

```text
CreateEmbeddingResponse(
    data=[
        Embedding(
            embedding=[-0.0055, 0.0178, 0.0151, ...],
            index=0,
            object='embedding'
        )
    ],
    model='text-embedding-3-small',
    object='list'
)
```

## Length of Embedding

```python
print("Length of embeddings :", len(response.data[0].embedding))
```

Output:

```text
Length of embeddings : 1536
```

Matlab hamare text ka meaning 1536 numbers ke vector mein represent ho raha hai.

## Should We Print Full Embedding Vector?

```python
# print("Embedding vector is :", response.data[0].embedding)
```

Maine ye line comment ki hai because embedding vector bahut long hota hai.

Learning ke liye ek baar print kar sakte ho, but normally full vector print nahi karte.

Normally hum embedding vector ko save karte hain:

```text
Vector database
Database
JSON file
CSV file
```

Then uska use similarity search ya RAG application mein karte hain.

## Example: Same Words, Different Order

Try these two sentences:

```python
text = "dog chases cat"
```

and

```python
text = "cat chases dog"
```

Dono mein words same hain:

```text
dog
chases
cat
```

But meaning different hai.

```text
dog chases cat
```

Means dog cat ko chase kar raha hai.

```text
cat chases dog
```

Means cat dog ko chase kar rahi hai.

So word order bhi important hota hai.

## Important Note

Sentence embeddings exactly same nahi honge, because embedding model full sentence ka meaning dekhta hai.

But ye example important hai because isse hume samajh aata hai ki sirf words enough nahi hain, words ka order and context bhi important hota hai.

## What Comes After Embeddings?

Embeddings ke baad model ke andar aur concepts aate hain:

```text
Positional Encoding
Self-Attention
Multi-Head Attention
Transformer Layers
```

Short meaning:

```text
Positional Encoding = token ki position samajhna
Self-Attention = tokens ek dusre se relation samajhte hain
Multi-Head Attention = same text ko multiple angles se samajhna
Transformer Layers = deeper context understanding
```

In sabko next lessons mein detail mein samjhenge.

## Small Note: Training vs Inference

LLM ke 2 phases hote hain:

```text
Training Phase = model ko train karna
Inference Phase = trained model ko use karna
```

Hum yahan jo OpenAI API use kar rahe hain, wo **inference phase** hai.

Matlab model already trained hai, and hum us model ka use karke embedding generate kar rahe hain.

## Conclusion

So basically, vector embeddings text ko meaning wale number format mein convert karte hain.

In my example, `text-embedding-3-small` model se embedding length 1536 aa rahi hai.

Embeddings ka use semantic search, similarity check, vector database, RAG, and AI apps mein hota hai.

Simple summary:

```text
Tokenization = text ko tokens mein todna
Embeddings = text ka meaning numbers mein convert karna
Inference = trained model ko use karna
```
