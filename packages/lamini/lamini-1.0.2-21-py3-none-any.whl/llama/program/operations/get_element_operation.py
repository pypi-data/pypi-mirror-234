from llama.program.value import Value

from llama.program.util.type_to_dict import value_to_dict, type_to_dict

import json


class GetElementOperation(Value):
    def __init__(self, input_value, type, element_index):
        super().__init__(type)
        self._element_index = element_index
        self._input_value = input_value

    def _to_dict(self):
        input_value = type_to_dict(self._input_value)
        return {
            "name": "GetElementOperation",
            "input_value": input_value,
            "type": type_to_dict(self._type),
            "element_index": self._element_index,
        }
