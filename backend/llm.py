import os
from dotenv import load_dotenv
from langchain_openai import ChatOpenAI

# Load the keys from the .env file
load_dotenv()

# Initialize the LLM just like in your notebook
llm = ChatOpenAI(
    model="meta/llama-3.1-70b-instruct", 
    api_key=os.getenv("NVIDIA_API_KEY"),
    base_url="https://integrate.api.nvidia.com/v1")