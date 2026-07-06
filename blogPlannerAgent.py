import os

from dotenv import load_dotenv
from google.adk import Context
from google.adk.agents import LlmAgent
from google.adk.workflow import node
from google.adk.models import LiteLlm

load_dotenv()
#MODEL = os.getenv("MODEL", "gemini-flash-latest")
MODEL = LiteLlm(model=os.getenv("MODEL", "groq/llama-3.3-70b-versatile"))

blog_planner = LlmAgent(
    name="BlogPlanner",
    model=MODEL,
    description="...",
    instruction="""
        ...
        """,
)



