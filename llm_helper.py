
from langchain_groq import ChatGroq
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

# Initialize LLM with Groq API key
llm = ChatGroq(groq_api_key=os.getenv("GROQ_API_KEY"), model_name="llama-3.2-90b-vision-preview")


if __name__ == "__main__":
    response = llm.invoke("Two most important ingredients in samosa are?")
    print(response.content)
