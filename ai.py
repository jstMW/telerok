from ollama import ChatResponse
from ollama import chat
ollama_model = "phi3:latest"


def chat_wrapper(question, id):
    response: ChatResponse = chat(model=ollama_model, messages=[
        {
            'role': 'user',
            'content': question,
        },
    ])

    return response.message.content
