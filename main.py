from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationSummaryMemory
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


# Load existing conversation summary if available
context = ""
if os.path.exists("conversation_summary.txt"):
    with open("conversation_summary.txt", "r") as file:
        context = file.read()
        if not context.strip():
            context = "This is the first conversation, we weren't talking before this"


# Initialize ConversationSummaryMemory with pre-loaded context
memory = ConversationSummaryMemory(llm=llm)

# Create a conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=False  # Set to True to see detailed logs
)

while True:
    # Pass the context before each user input so the model knows what we were talking about
    memory.save_context({"input": ""}, {"output": context})
    user_input = input("You: ")
    if user_input == "exit":
        break
    response = conversation.predict(input=user_input)
    # Save the context after each user input
    context=memory.load_memory_variables({})["history"]
    print("Bot:", response)

    

with open("conversation_summary.txt", "w") as file:
    file.write(memory.load_memory_variables({})["history"])
