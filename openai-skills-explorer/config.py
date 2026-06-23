import os
from dotenv import load_dotenv
from openai import OpenAI

load_dotenv()

client = OpenAI(
    api_key = os.getenv("Azure_OPENAI_KEY"),
    base_url = os.getenv("Azure_OPENAI_ENDPOINT"),
)
MODEL = os.getenv("AZURE_OPENAI_MODEL")
