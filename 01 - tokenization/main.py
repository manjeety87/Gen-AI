import tiktoken

encoder = tiktoken.encoding_for_model("gpt-4o")

text ="Hello, I am Mann"

tokens = encoder.encode(text)
print("Tokens:", tokens)

tokens = [13225, 11, 357, 939, 23959]

decoded = encoder.decode(tokens)
print("Decoded normal text is :", decoded)