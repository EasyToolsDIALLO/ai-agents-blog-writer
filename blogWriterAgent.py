import os

from dotenv import load_dotenv
from google.adk import Context
from google.adk.agents import LlmAgent
from google.adk.workflow import node
from google.adk.models import LiteLlm

load_dotenv()
#MODEL = os.getenv("MODEL", "gemini-flash-latest")
MODEL = LiteLlm(model=os.getenv("MODEL", "groq/llama-3.3-70b-versatile"))

blog_writer = LlmAgent(
    name="BlogWriter",
    model=MODEL,
    description="Écrit un article technique à partir de l'outline.",
    instruction="""
        Écris un article Markdown complet à partir de l'outline fourni.

        Guidelines:
        - Audience: software engineers; skip basics and focus on practical insight.
        - Explain both the 'how' and 'why'.
        - Include concise code snippets when helpful.
        - Follow the outline's structure (H2/H3).
        - Output only the final article in Markdown.
        """,
)

post_validator = LlmAgent(
    name="BlogPostValidationChecker",
    model=MODEL,
    description="Valide le post final.",
    instruction="""
        Vérifie l'article fourni : introduction, sections claires
        correspondant à l'outline, conclusion, et clarté technique.
        Si ça passe, réponds exactement "ok".
        Sinon réponds "retry" avec les corrections spécifiques.
        """,
)

@node(name="RobustBlogWriter", rerun_on_resume=True)
async def robust_blog_writer(ctx: Context, node_input: str) -> str:
    outline = node_input  # ← sortie du nœud RobustBlogPlanner

    post = await ctx.run_node(blog_writer, outline)

    for _ in range(3):
        verdict = await ctx.run_node(post_validator, post)
        if str(verdict).strip().lower().startswith("ok"):
            break
        post = await ctx.run_node(
            blog_writer,
            f"Outline:\n{outline}\n\nBrouillon actuel:\n{post}\n\nCorrections demandées: {verdict}\nRéécris l'article corrigé.",
        )

    return post