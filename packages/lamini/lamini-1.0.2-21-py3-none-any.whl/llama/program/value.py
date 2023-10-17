from llama.types.base_specification import BaseSpecification
from llama.program.util.run_ai import query_run_program


class Value(object):
    def __init__(self, type, data=None):
        self._type = type
        self._data = data
        self._function = None
        self._index = None

    def _get_field(self, name):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        return self._data._get_attribute_raw(name)

    def __str__(self):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        return str(self._data)

    def __int__(self):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        return int(self._data)

    def __float__(self):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        return float(self._data)

    def __gt__(self, other):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        if isinstance(other, Value):
            other = other._get_data()

        return self._data > other

    def _get_data(self):
        if self._data is None:
            raise Exception("Value Access Error: must compute value before acessing")

        return self._data

    def __repr__(self):
        return str(self)

    def _compute_value(self):
        # check in the builder value cache
        if self._index in self._function.program.builder.value_cache:
            returned_value = self._function.program.builder.value_cache[self._index][
                "data"
            ]
        else:
            params = {
                "program": self._function.program.to_dict(),
                "requested_values": [self._index],
            }
            response = query_run_program(params)

            response.raise_for_status()

            # update the cache
            self._function.program.builder.value_cache.update(response.json())

            returned_value = response.json()[str(self._index)]["data"]

        if issubclass(self._type, BaseSpecification):
            self._data = self._type.parse_obj(returned_value)
        else:
            self._data = self._type(returned_value)

    def __getattribute__(self, name):
        if name.find("_") == 0:
            return super().__getattribute__(name)

        return self._function.program.builder.get_field(self, name)

    def _get_attribute_raw(self, name):
        return super().__getattribute__(name)
