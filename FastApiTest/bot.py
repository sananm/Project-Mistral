from langchain_community.chat_models import ChatOpenAI
from langchain.memory import ConversationBufferMemory, ConversationSummaryMemory
from langchain.chains import ConversationChain
from langchain.callbacks.streaming_stdout import StreamingStdOutCallbackHandler
from langchain.schema import messages_to_dict, messages_from_dict
from dotenv import load_dotenv
import os
import json
class GPT():
    
    def __init__(self):
        # Set your custom endpoint
        os.environ["OPENAI_API_KEY"] = "not-needed"  # LM Studio doesn't require a real key
        os.environ["OPENAI_BASE_URL"] = "http://localhost:1234/v1"

        self.llm = ChatOpenAI(
            temperature=0.7,
            model_name="mistral-7b-instruct-v0.3",  # Name doesn't matter much for LM Studio
            openai_api_base=os.environ["OPENAI_BASE_URL"],
            openai_api_key=os.environ["OPENAI_API_KEY"],
            streaming=True,
            callbacks= [StreamingStdOutCallbackHandler()]
        )
        self.memory = ConversationSummaryMemory(llm=self.llm)

        self.context = ""

        # Load and restore it into a new memory instance
        if os.path.exists("info/summary_memory.txt"):
            with open("info/summary_memory.txt", "r") as f:
                context = f.read()
                print(context)

            self.memory.buffer = context  # Restore the memory summary
        # Create a conversation chain with memory
        self.conversation = ConversationChain(
            llm=self.llm,
            memory= self.memory
        )
    
    def ask(self, prompt = None):
        response = self.conversation.predict(input=prompt)
        return response
    
    def exit(self):
        with open("info/summary_memory.txt", "w") as f:
            f.write(self.memory.buffer)

        history = self.memory.chat_memory.messages
        with open("info/conversation_history.json", "w") as f:
            json.dump(messages_to_dict(history), f)

