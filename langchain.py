
import os
from langchain.chat_models import init_chat_model

GEMINI_API_KEY = 'my-google/openai/claude-antropic-api-key'
os.environ["GOOGLE_API_KEY"] = GEMINI_API_KEY
#os.environ["OPENAI_API_KEY"] = "sk-..."
#os.environ["OLLAMA_HOST"] = "http://localhost:11434"

model = init_chat_model("google_genai:gemini-2.5-flash")
#model = init_chat_model("openai:gpt-4o-mini")
#model = init_chat_model("ollama:llama3.2:1b")

# conversation = [
#     {"role": "system", "content": "You are a helpful assistant that translates English to French."}, #system = context
#     {"role": "user", "content": "Translate: I love programming."},                                   #user = client sending questions
#     {"role": "assistant", "content": "J'adore la programmation."},                                   #assistant = ai that anwser back
#     {"role": "user", "content": "Translate: I love building applications."}                          #user = can ask again
# ]

# response = model.invoke(conversation)
response = model.invoke("Qual o plano free do google gemini 20.5 flash? Qual sua capacidade no free tier? estou usando sua api")

print(response) #object response it has token usage, content and general meta data
print("--------------")
print(response.content) #content from object response
