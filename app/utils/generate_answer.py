from llm.llm_factory import LLMRunnerFactory


def generate_answer(
        prompt,
        llm_name="gemini"):

    llm_runner = (
        LLMRunnerFactory.create_runner(
            llm_name
        )
    )

    answer = llm_runner.run_prompt(
        prompt
    )

    return answer