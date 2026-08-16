from ollama import chat
from ollama import ChatResponse

class LLM:
    def __init__(self):
        pass

    def ask(self, question):
        response: ChatResponse = chat(model='qwen2.5:14b', messages=[
          {
            'role': 'user',
            'content': question,
          },
        ])

        return response['message']['content']
