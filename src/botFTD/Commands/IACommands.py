from langchain.llms import OpenAI
import os 
from dotenv import load_dotenv , find_dotenv

load_dotenv(find_dotenv())

openAI_LLM = OpenAI(temperature=0, openai_api_key=os.getenv("OPEN_AI_KEY"))


def askCommand(ctx, text):
    output = openAI_LLM(text)
    return ctx.send(output)