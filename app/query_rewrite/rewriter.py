from app.llm.generate_answer import generate_answer
from app.utils.prompt_builder import build_prompt
from app.utils.generate_answer import generate_answer

def rewrite_query(
    current_query,
    chat_history
):
    prompt = bulld_prompt( 
    "query_rewrite.txt",
    current_query,
    chat_history
    )

    return generate_answer(prompt).strip()