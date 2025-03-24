from langchain.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import messages_to_dict, messages_from_dict
from dotenv import load_dotenv
import os
import json

# Set your custom endpoint
os.environ["OPENAI_API_KEY"] = "not-needed"  # LM Studio doesn't require a real key
os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1"

llm = ChatOpenAI(
    temperature=0.7,
    model_name="mistral-7b-instruct-v0.3",  # Name doesn't matter much for LM Studio
    openai_api_base=os.environ["OPENAI_BASE_URL"],
    openai_api_key=os.environ["OPENAI_API_KEY"],
    streaming=True,
    callbacks= [StreamingStdOutCallbackHandler()]
)
memory = ConversationSummaryMemory(llm=llm)

context = ""

# Load and restore it into a new memory instance
if os.path.exists("summary_memory.txt"):
    with open("summary_memory.txt", "r") as f:
        context = f.read()
        print(context)

    memory.buffer = context  # Restore the memory summary
# Create a conversation chain with memory
conversation = ConversationChain(
    llm=llm,
    memory=memory,
    verbose=True  # Set to True to see detailed logs
)

while True:
    # memory.save_context({"input":""}, {"output": context})
    user_input = input("You: ")
    if user_input == "b6gd":
        break
    print("\nviksit: ", end=" ")
    response = conversation.predict(input=user_input)
    context = memory.buffer
    # print("Viksit: ",response)
    

# Save the summary buffer to a file
with open("summary_memory.txt", "w") as f:
    f.write(memory.buffer)

history = memory.chat_memory.messages
with open("conversation_history.json", "w") as f:
    json.dump(messages_to_dict(history), f)

memory.clear()