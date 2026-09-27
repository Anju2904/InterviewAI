import ollama

response = ollama.chat(
    model="llama3",
    messages=[
        {
            "role": "user",
            "content": "Generate one Python Developer interview question."
        }
    ]
)

print(
    response["message"]["content"]
)