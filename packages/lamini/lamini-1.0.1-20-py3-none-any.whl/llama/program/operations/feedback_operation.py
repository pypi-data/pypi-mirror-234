from llama.program.value import Value
from llama.types.type import Type
from llama.types.context import Context

from llama.program.util.type_to_dict import value_to_dict

import json


class FeedbackType(Type):
    result: bool = Context("The result of the feedback test")


class FeedbackOperation(Value):
    def __init__(
        self, on, to, good_examples=[], bad_examples=[], temperature=0.0, version=""
    ):
        super().__init__(FeedbackType)
        self._on = on
        self._to = to
        self._good_examples = good_examples
        self._bad_examples = bad_examples
        self._temperature = temperature
        self._version = version

    def _to_dict(self):
        return {
            "name": "FeedbackOperation",
            "on": self._on,
            "to": self._to,
            "good_examples": [
                value_to_dict(example) for example in self._good_examples
            ],
            "bad_examples": [value_to_dict(example) for example in self._bad_examples],
            "temperature": self._temperature,
            "type": json.loads(self._type.schema_json()),
            "version": self._version,
        }

    def __str__(self):
        return str(self._to_dict())
