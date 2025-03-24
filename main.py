from langchain.chat_models import ChatOpenAI
from langchain.schema import HumanMessage
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

response = llm([HumanMessage(content="Explain LangChain in simple terms")])
print(response.content)