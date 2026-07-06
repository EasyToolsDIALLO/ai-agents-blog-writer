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
    description="Crée un outline pratique et facile à lire en Markdown.",
    instruction="""
        Tu es un stratège de contenu technique. Produis un outline Markdown clair avec:
        - Title
        - Short intro
        - 4–6 main sections (each with 2–3 bullets)
        - Conclusion

        Si un feedback de validation est fourni, corrige les éléments manquants.
        Retourne uniquement l'outline en Markdown.
        """,
)

outline_validator = LlmAgent(
    name="OutlineValidationChecker",
    model=MODEL,
    description="Valide que l'outline est utilisable.",
    instruction="""
        Vérifie l'outline fourni. S'il a un titre, une introduction,
        4–6 sections et une conclusion, réponds exactement "ok".
        Sinon réponds "retry" suivi de la liste des éléments manquants.
        """,
)

@node(name="RobustBlogPlanner", rerun_on_resume=True)
async def robust_blog_planner(ctx: Context, node_input: str) -> str:
    topic = node_input  # ← message utilisateur, converti en str automatiquement

    outline = await ctx.run_node(blog_planner, topic)

    for _ in range(3):
        verdict = await ctx.run_node(outline_validator, outline)
        if str(verdict).strip().lower().startswith("ok"):
            break
        outline = await ctx.run_node(
            blog_planner,
            f"Sujet: {topic}\nFeedback: {verdict}\nCorrige l'outline.",
        )

    return outline