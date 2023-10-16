import os
import sys
from pathlib import Path

def user_dir():
    llm_user_path = os.environ.get("NLLM_USER_PATH")
    if llm_user_path:
        path = Path(llm_user_path)
    else:
        path = Path(os.path.expanduser("~/.nanollm"))
    path.mkdir(exist_ok=True, parents=True)
    return path

def read_prompt(prompt):
    # Is there extra prompt available on stdin?
    stdin_prompt = None
    if not sys.stdin.isatty():
        stdin_prompt = sys.stdin.read()

    if stdin_prompt:
        bits = [stdin_prompt]
        if prompt:
            bits.append(prompt)
        prompt = " ".join(bits)

    if prompt is None and sys.stdin.isatty():
        # Hang waiting for input to stdin (unless --save)
        prompt = sys.stdin.read()
    return prompt