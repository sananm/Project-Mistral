from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory
from langchain.chains import ConversationChain
from dotenv import load_dotenv
import os


# Set your custom endpoint
os.environ["OPENAI_API_KEY"] = "not-needed"  # LM Studio doesn't require a real key
os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1"

llm = ChatOpenAI(
    temperature=0.7,
    model_name="mistral-7b-instruct-v0.3",  # Name doesn't matter much for LM Studio
    openai_api_base=os.environ["OPENAI_BASE_URL"],
    openai_api_key=os.environ["OPENAI_API_KEY"]
)

memory = ConversationBufferMemory()

# Create a conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Set to True to see detailed logs
)


response1 = conversation.predict(input="Hi, who are you?")
print(response1)

response2 = conversation.predict(input="What can you do?")
print(response2)

response3 = conversation.predict(input="What did I ask you earlier?")
print(response3)

response4 = conversation.predict(input="Did I also not ask you about your capabilities?")
print(response4)