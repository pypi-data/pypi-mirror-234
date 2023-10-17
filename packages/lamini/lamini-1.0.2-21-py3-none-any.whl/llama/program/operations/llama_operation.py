from llama.program.value import Value

from llama.program.util.type_to_dict import value_to_dict

import json


class LlamaOperation(Value):
    def __init__(self, input_value, output_type, *args, **kwargs):
        super().__init__(output_type)
        self._input_value = input_value
        self._args = {"args": args, "kwargs": kwargs}

    def _to_dict(self):
        input_value = value_to_dict(self._input_value)
        return {
            "name": "LlamaOperation",
            "input_value": input_value,
            "type": json.loads(self._type.schema_json()),
            "args": self._args,
        }
