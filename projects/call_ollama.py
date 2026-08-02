# import requests

# r = requests.post(
#   "http://localhost:11434/api/generate",
#   json={"model": "llama3.2",
#         "prompt": "Hello, who is pm of Nepal!",
#         "stream": False})
# print(r.json()["response"])

# or use the official python client:
# pip install ollama
import ollama
response = ollama.generate(
    model="llama3.2",
    prompt="Hello, who is pm of Nepal!"
)
print(response["response"])
