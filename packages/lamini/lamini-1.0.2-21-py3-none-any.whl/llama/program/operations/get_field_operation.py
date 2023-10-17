from llama.program.value import Value

from llama.program.util.type_to_dict import value_to_dict, type_to_dict

import json


class GetFieldOperation(Value):
    def __init__(self, input_value: Value, output_type: type, field_name: str):
        super().__init__(output_type)
        self._field_name = field_name
        self._input_value = input_value

    def _to_dict(self):
        input_value = value_to_dict(self._input_value)
        return {
            "name": "GetFieldOperation",
            "input_value": input_value,
            "type": type_to_dict(self._type),
            "field_name": self._field_name,
        }
