from llama.program.value import Value

from llama.program.util.type_to_dict import type_to_dict


class GetArgumentOperation(Value):
    def __init__(self, type, input_value_index):
        super().__init__(type)
        self._input_value_index = input_value_index

    def _to_dict(self):
        return {
            "name": "GetArgumentOperation",
            "input_value": {
                "index": self._input_value_index,
                "type": type_to_dict(self._type),
            },
        }
