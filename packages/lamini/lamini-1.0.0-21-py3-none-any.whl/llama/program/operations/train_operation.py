from llama.program.value import Value


class TrainOperation(Value):
    def __init__(self, *args, **kwargs):
        self._args = {"args": args, "kwargs": kwargs}

    def _to_dict(self):
        return {
            "name": "TrainOperation",
            "args": self._args,
        }
