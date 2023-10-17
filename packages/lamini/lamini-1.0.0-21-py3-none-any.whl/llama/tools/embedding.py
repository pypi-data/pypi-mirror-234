from typing import List, Union
from llama.program.util.run_ai import query_run_embedding


class Embedding:
    def get_embedding(prompt: Union[str, List[str]]):
        return query_run_embedding(prompt)
