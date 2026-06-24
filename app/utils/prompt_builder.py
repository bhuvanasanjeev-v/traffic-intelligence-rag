from llm.prompt_loader import load_prompt_template


def build_prompt(
        prompt_name,
        context,
        query):

    prompt_template = load_prompt_template(
        prompt_name
    )

    prompt = prompt_template.format(
        context=context,
        query=query
    )

    return prompt