from pathlib import Path


PROMPTS_DIR = Path(__file__).parent / "prompts"


def load_prompt_template(prompt_name: str) -> str:
    prompt_path = PROMPTS_DIR / prompt_name

    if not prompt_path.exists():
        raise FileNotFoundError(f"Prompt file not found: {prompt_path}")

    return prompt_path.read_text(encoding="utf-8")
