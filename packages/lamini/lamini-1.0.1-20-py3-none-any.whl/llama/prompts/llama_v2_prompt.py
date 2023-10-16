from llama.prompts.prompt import BasePrompt
from llama import Type, Context


class LlamaV2Input(Type):
    system: str = Context(" ")
    user: str = Context(" ")


class LlamaV2Output(Type):
    output: str = Context(" ")


class LlamaV2Prompt(BasePrompt):
    prompt_template = """[INST] <<SYS>>
{input:system}
<</SYS>>
{input:user} [/INST]"""
