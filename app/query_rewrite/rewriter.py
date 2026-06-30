from app.utils.prompt_builder import build_prompt
from app.utils.generate_answer import generate_answer


def rewrite_query(
    current_query,
    chat_history,
    answer_fn=generate_answer,
):
    prompt = build_prompt(
        "query_rewrite.txt",
        current_query=current_query,
        chat_history=format_chat_history(chat_history),
    )

    return answer_fn(prompt).strip()


def format_chat_history(chat_history):
    if not chat_history:
        return "No previous conversation."

    return "\n".join(
        f"{message['role']}: {message['content']}"
        for message in chat_history
    )
