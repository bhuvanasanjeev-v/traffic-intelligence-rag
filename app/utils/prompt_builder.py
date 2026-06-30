from llm.prompt_loader import load_prompt_template


def build_prompt(
        prompt_name,
        context=None,
        query=None,
        **kwargs):

    prompt_template = load_prompt_template(
        prompt_name
    )

    prompt_values = {
        "context": context,
        "query": query,
        **kwargs,
    }

    prompt = prompt_template.format(
        **prompt_values
    )

    return prompt
