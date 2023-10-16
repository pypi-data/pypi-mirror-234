from llama.program.value import Value

from llama.program.util.type_to_dict import value_to_dict

import json


class MetricOperation(Value):
    def __init__(self, input_value, output_type):
        super().__init__(output_type)
        self._input_value = input_value

    def to_dict(self):
        input_value = value_to_dict(self._input_value)

        return {
            "name": "MetricOperation",
            "input_value": input_value,
            "type": json.loads(self._type.schema_json()),
        }
