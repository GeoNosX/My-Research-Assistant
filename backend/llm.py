import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the keys from the .env file
load_dotenv()

# Initialize the LLM just like in your notebook
llm = ChatOpenAI(
    model_name="nvidia/nemotron-3-nano-30b-a3b:free",
    openai_api_key=os.getenv("OPENROUTER_API_KEY"),
    openai_api_base="https://openrouter.ai/api/v1",
    temperature=0.0
)