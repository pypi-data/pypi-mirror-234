from typing import List, Optional
from llama.program.function import Function
from llama.program.util.type_to_dict import value_to_dict, data_to_dict
from llama.prompts.prompt import BasePrompt


class Program:
    """Internal representation of a program that can be executed by the Llama
    large language model engine.

    Each program has a unique name (within your account).

    """

    def __init__(self, builder, name: str, prompt: Optional[BasePrompt]):
        self.builder = builder
        self.name = name
        self.main = Function(program=self, name="main")
        self.functions = {"main": self.main}
        self.examples = []
        self.prompt = prompt

    def add_data(self, examples: List):
        if isinstance(examples, list):
            self.examples.extend(examples)
        else:
            # singleton
            self.examples.append(examples)

    def add_metric(self, metric):
        self.add_operation(metric)

    def to_dict(self):
        examples = data_to_dict(self.examples)
        dict_object = {
            "name": self.name,
            "functions": {
                name: function.to_dict() for name, function in self.functions.items()
            },
            "examples": examples,
        }
        if self.prompt:
            dict_object["templates"] = {}
            dict_object["templates"]["prompt"] = self.prompt.prompt_template
        return dict_object
