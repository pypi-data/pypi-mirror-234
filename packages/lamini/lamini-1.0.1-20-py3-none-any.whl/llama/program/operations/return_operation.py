from llama.program.value import Value

from llama.program.util.type_to_dict import value_to_dict


class ReturnOperation(Value):
    def __init__(self, output_value):
        super().__init__(get_type(output_value))
        self._output_value = output_value

    def _to_dict(self):
        if isinstance(self._output_value, tuple):
            output_value = [value_to_dict(value) for value in self._output_value]
        else:
            output_value = value_to_dict(self._output_value)

        return {
            "name": "ReturnOperation",
            "output_value": output_value,
        }


def get_type(output_value):
    if isinstance(output_value, tuple):
        return (value._type for value in output_value)

    return output_value._type
