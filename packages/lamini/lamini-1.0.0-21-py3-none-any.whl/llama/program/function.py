from llama.program.operations.get_argument_operation import GetArgumentOperation


class Function:
    def __init__(self, program, name, input_arguments=[]):
        self.name = name
        self.program = program
        self.operations = []

        for index, argument in enumerate(input_arguments):
            self.add_operation(GetArgumentOperation(argument, index))

    def add_operation(self, operation):
        operation._index = len(self.operations)
        operation._function = self

        self.operations.append(operation)

        return operation

    def to_dict(self):
        dict_object = {
            "name": self.name,
            "operations": [operation._to_dict() for operation in self.operations],
        }
        return dict_object
