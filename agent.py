import os
import datetime

from dotenv import load_dotenv
from google.adk.agents import LlmAgent
from google.adk.workflow import Workflow
from google.adk.models import LiteLlm

from .blogPlannerAgent import robust_blog_planner
from .blogWriterAgent import robust_blog_writer

load_dotenv()
#MODEL = os.getenv("MODEL", "gemini-flash-latest")
MODEL = LiteLlm(model=os.getenv("MODEL", "groq/llama-3.3-70b-versatile"))

finalizer = LlmAgent(
    name="Finalizer",
    model=MODEL,
    description="Formate et enrichit l'article final avec titres alternatifs et hooks de tweet.",
    instruction=f"""
        À partir du brouillon d'article fourni, retourne:
        1) L'article complet inchangé
        2) 3 titres alternatifs
        3) 2 hooks de tweet

        Date: {datetime.datetime.now().strftime("%Y-%m-%d")}
        """,
)

root_agent = Workflow(
    name="Blogger",
    edges=[
        ("START", robust_blog_planner, robust_blog_writer, finalizer),
    ],
)