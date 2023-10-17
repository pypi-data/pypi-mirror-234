import os
import time
from typing import List, Optional
from llama.program.program import Program
from llama.program.function import Function
from llama.program.util.config import edit_config
from llama.program.util.run_ai import (
    query_run_program,
    fuzzy_is_duplicate,
    query_run_embedding,
    get_ui_url,
)

from llama.types.type import Type

from llama.program.operations.llama_operation import LlamaOperation
from llama.program.operations.batch_llama_operation import BatchLlamaOperation
from llama.program.operations.metric_operation import MetricOperation
from llama.program.operations.call_operation import CallOperation
from llama.program.operations.get_element_operation import GetElementOperation
from llama.program.operations.get_field_operation import GetFieldOperation
from llama.program.operations.return_operation import ReturnOperation
from llama.program.operations.feedback_operation import FeedbackOperation

import inspect

from llama.program.util.api_actions import (
    gen_queue_batch,
    gen_submit_data,
    gen_submit_training_job,
    gen_inference_job_status,
    gen_inference_job_results,
    gen_cancel_job,
    gen_multiple_values,
    gen_value,
    gen_clear_data,
    gen_training_job_status,
    gen_all_training_job_status,
    gen_cancel_training_job,
    gen_cancel_training_jobs,
    gen_training_eval,
)
from llama.prompts.prompt import BasePrompt
from llama.program.util.type_to_dict import data_to_dict


class Builder:
    """Build a program for execution by the Llama large language model engine."""

    def __init__(
        self,
        id: str = "default_dataset",
        model_name: Optional[str] = None,
        prompt: Optional[BasePrompt] = None,
        key: Optional[str] = None,
        config: dict = {},
    ):
        assert isinstance(model_name, str) or model_name is None

        self.id = id
        self.program = Program(self, id, prompt)
        self.current_function = self.program.main
        self.value_cache = {}
        self.model_name = model_name
        self.prompt = prompt
        self.training_job_id = None
        self.key = key
        self.config = config
        if "use_num_gpus" not in self.config:
            self.config["use_num_gpus"] = 1

        if self.key is not None:
            self.config.update({"production": {"key": self.key}})
        edit_config(self.config)

    def __call__(self, input, output_type, *args, **kwargs):
        """Inference with the LLM. input can be a single value or a list of values."""
        # Reset program
        self.program = Program(self, self.id, self.prompt)
        self.current_function = self.program.main
        if isinstance(input, list):
            values = self.add_model(input, output_type, *args, **kwargs)
            results = gen_multiple_values(values)
            if isinstance(results[0], list):
                return [value for sublist in results for value in sublist]
            return results
        else:
            value = self.add_model(input, output_type, *args, **kwargs)
            result = gen_value(value)
            return result

    def add_model(self, input, output_type, *args, **kwargs):
        if isinstance(input, list):

            def partition(l, n):
                for i in range(0, len(l), n):
                    yield l[i : i + n]

            chunks = list(partition(input, self.config["use_num_gpus"] * 20))
            if self.model_name is not None:
                kwargs["model_name"] = self.model_name
            operations = []
            for chunk in chunks:
                new_operation = self.current_function.add_operation(
                    BatchLlamaOperation(chunk, output_type, *args, **kwargs)
                )
                operations.append(new_operation)
            return operations
        else:
            if self.model_name is not None:
                kwargs["model_name"] = self.model_name
            new_operation = self.current_function.add_operation(
                LlamaOperation(input, output_type, *args, **kwargs)
            )
            return new_operation

    def train(self, data: list = None, **kwargs):
        """Training a LLM."""

        job = self.submit_training_job(data, **kwargs)
        url = get_ui_url()
        print(
            f"Training job submitted! Check status of job {job['job_id']} here: {url}/train/{job['job_id']}"
        )

        try:
            status = self.get_training_job_status(job["job_id"])
            if status["status"] == "FAILED":
                print(f"Job failed: {status}")
                return status

            while status["status"] not in ("COMPLETED", "FAILED", "CANCELLED"):
                if kwargs.get("verbose", False):
                    print(f"job not done. waiting... {status}")
                time.sleep(30)
                status = self.get_training_job_status(job["job_id"])
                if status["status"] == "FAILED":
                    print(f"Job failed: {status}")
                    return status
                elif status["status"] == "CANCELLED":
                    print(f"Job canceled: {status}")
                    return status
            print(
                f"Finetuning process completed, model name is: {status['model_name']}"
            )
        except KeyboardInterrupt as e:
            print("Cancelling job")
            return self.cancel_training_job(job["job_id"])
        return status

    def eval(self, training_job_id: str = None):
        """Get Training Eval Results"""

        if training_job_id is None:
            training_job_id = self.training_job_id
        if training_job_id is None:
            raise Exception("Must train before getting results (no training job id))")
        return gen_training_eval(training_job_id)

    def evaluate(self):
        """Get Training Eval Results"""
        return self.eval()

    def submit_inference_job(self, input, output_type, *args, **kwargs):
        """Submit a large batch of inputs for inference."""
        if isinstance(input, list):
            values = self.add_model(input, output_type, *args, **kwargs)
            results = gen_queue_batch(values)
            return results
        else:
            new_input = [input]
            values = self.add_model(new_input, output_type, *args, **kwargs)
            results = gen_queue_batch(values)
            return results

    def submit_training_job(self, data: list = None, **kwargs):
        """Submit a training job."""
        templates = None
        if self.prompt:
            templates = {
                "prompt": self.prompt.prompt_template,
            }
        serialized_data = data_to_dict(data)
        results = gen_submit_training_job(
            self.id,
            self.model_name,
            serialized_data,
            kwargs.get("task", None),
            kwargs.get("enable_peft", False),
            kwargs.get("finetune_args", {}),
            kwargs.get("peft_args", {}),
            kwargs.get("is_public", False),
            kwargs.get("use_cached_model", True),
            templates,
        )
        training_job_id = results["job_id"]
        self.training_job_id = training_job_id

        if kwargs.get("verbose", False):
            print(f"job id: {self.training_job_id}")
        # wait until data part is done
        results = self.get_training_job_status(training_job_id)
        return results

    def get_inference_job_status(self, job_id: str):
        """Get the status of a batch inference job."""
        if job_id is None:
            raise Exception("Must train before getting results (no training job id))")
        status = gen_inference_job_status(job_id)
        return status

    def get_training_job_status(self, job_id: int = None):
        """Get the status of a training job."""
        if job_id is None and self.training_job_id is None:
            raise Exception("Must train before getting results (no training job id))")
        elif job_id is None:
            job_id = self.training_job_id
        status = gen_training_job_status(job_id)
        return status

    def list_all_training_jobs(
        self,
    ):
        """List all training jobs."""
        results = gen_all_training_job_status()
        return results

    def get_inference_job_results(self, job_id: str, output_type=None):
        """Get the results of a batch inference job as a list of `output_type` values"""
        results = gen_inference_job_results(job_id, output_type)
        return results

    def cancel_inference_job(
        self,
        inference_job_id: str = None,
    ):
        """Cancel a running inference job"""
        results = gen_cancel_job(inference_job_id)
        return results

    def cancel_training_job(
        self,
        job_id: int = None,
    ):
        """Cancel a training job"""
        if job_id is None and self.training_job_id is None:
            raise Exception("Must train before getting results (no training job id))")
        elif job_id is None:
            job_id = self.training_job_id
        results = gen_cancel_training_job(job_id)
        return results

    def cancel_all_training_jobs(
        self,
    ):
        """Cancel all training jobs"""
        results = gen_cancel_training_jobs()
        return results

    def sample(
        self,
        input,
        output_type,
        n: int = 1,
        max_similarity: float = 0.99,
        *args,
        **kwargs,
    ):
        """
        Generate n sample outputs from the LLM.
        Use max_similarity to control how similar the outputs are to each other.
        Higher values for max_similarity will result in more similar outputs.
        max_similarity should be between 0 and 1 and is the maximum cosine distance.
        """
        input_value = input
        if self.model_name is not None:
            kwargs["model_name"] = self.model_name
        new_operations = []
        cache_len = 5  # NOTE: should use actual cache length
        max_iter = cache_len
        temperature = 0.7  # NOTE: should use actual random temperature
        random = True
        attributes = [
            attribute
            for attribute, field in output_type.__fields__.items()
            if field.type_ == str
        ]
        attribute_embeddings = {attribute: [None, []] for attribute in attributes}
        for i in range(n):
            new_operation = None
            attribute_embeddings = {
                attribute: [None, embeddings[1]]
                for attribute, embeddings in attribute_embeddings.items()
            }
            j = 0
            while any(
                [
                    fuzzy_is_duplicate(
                        attribute_embedding,
                        attribute_reference_embeddings,
                        max_similarity,
                    )
                    for attribute_embedding, attribute_reference_embeddings in attribute_embeddings.values()
                ]
            ) or fuzzy_is_duplicate(
                list(attribute_embeddings.values())[0][0],
                [
                    attribute_embedding
                    for attribute_embedding, _ in list(attribute_embeddings.values())[
                        1:
                    ]
                ],
                max_similarity,
            ):
                if j == max_iter:
                    max_iter += cache_len
                    random = False
                    temperature += 0.1  # NOTE: this could be set differently
                new_operation = self.current_function.add_operation(
                    LlamaOperation(
                        input_value,
                        output_type,
                        random=random,
                        temperature=temperature,
                        *args,
                        **kwargs,
                    )
                )
                new_operation = gen_value(new_operation)
                for attribute in attributes:
                    attribute_embeddings[attribute][0] = query_run_embedding(
                        getattr(new_operation, attribute)
                    )
                j += 1
            if j == max_iter:
                continue
            for (
                attribute_embedding,
                attribute_reference_embeddings,
            ) in attribute_embeddings.values():
                attribute_reference_embeddings.append(attribute_embedding)
            if not new_operation:
                new_operation = self.current_function.add_operation(
                    LlamaOperation(
                        input_value,
                        output_type,
                        random=random,
                        temperature=temperature,
                        *args,
                        **kwargs,
                    )
                )
                new_operation = gen_value(new_operation)
            new_operations.append(new_operation)

        return new_operations

    def add_data(self, data):
        """
        Save the data available for the model during inference and training.
        """
        self.save_data(data)

    def save_data(self, data):
        """
        Save the data available for the model during inference and training.
        """
        if not isinstance(data, list):
            data = [data]
        data = [
            datum[0] if isinstance(datum, list) and len(datum) == 1 else datum
            for datum in data
        ]
        self.program.examples = []
        self.program.add_data(examples=data)
        results = gen_submit_data(self.program, self.id)
        return results

    def clear_data(self):
        """
        Clear the data available for the model during inference and training.
        """
        return gen_clear_data(self.id)

    def improve(
        self,
        on: str,
        to: str,
        good_examples: List = [],
        bad_examples: List = [],
        temperature: float = 0.0,
        version: str = "",
    ):
        """
        Seed the model inference with a preemptive "improve *field* by *criteria*".
        Parameters:
        - on: the field to improve
        - to: natural language description of the criteria to improve the field
        - good_examples: a list of examples of the field that pass the criteria
        - bad_examples: a list of examples of the field that fail the criteria
        - temperature: the temperature to use for the model inference
        """
        new_operation = self.current_function.add_operation(
            FeedbackOperation(
                on=on,
                to=to,
                good_examples=good_examples,
                bad_examples=bad_examples,
                temperature=temperature,
                version=version,
            )
        )

        return new_operation

    def function(self, function):
        """
        Decorator to define a function that can be called from the LLM.
        """
        signature = inspect.signature(function)
        input_types = [value.annotation for value in signature.parameters.values()]

        main = self.current_function
        new_function = Function(
            program=self.program, name=function.__name__, input_arguments=input_types
        )
        self.program.functions[new_function.name] = new_function
        self.current_function = new_function
        output_value = function(*new_function.operations)
        self.current_function.add_operation(ReturnOperation(output_value))
        self.current_function = main

        return Lambda(self, new_function, output_value)

    def parallel(self, function):
        """
        Decorator to define a function that can be called from the LLM.
        """
        return self.function(function=function)

    def add_call(self, function, input_value, output_value):
        """
        Add a function that can be called from the LLM.
        """
        new_operation = self.current_function.add_operation(
            CallOperation(function, input_value, output_value)
        )

        result = new_operation

        if isinstance(output_value, tuple):
            result = []

            for index, value in enumerate(output_value):
                result.append(
                    self.current_function.add_operation(
                        GetElementOperation(new_operation, value.type, index)
                    )
                )

        return result

    def get_field(self, value, field_name):
        """
        Operation to get a field from a value
        """
        return self.current_function.add_operation(
            GetFieldOperation(
                value, value._type._get_field_type(field_name), field_name
            )
        )

    def add_metric(self, metric):
        """
        Operation to add a metric operation
        """
        new_operation = self.current_function.add_operation(
            MetricOperation(metric.input, metric.get_metric_type())
        )

        return new_operation

    def make_metric(
        self, input: Type, metric_type: type, fit: bool = True, higher_is_better=True
    ):
        """
        Operation to make a metric operation
        """
        new_operation = self.current_function.add_operation(
            MetricOperation(input, metric_type)
        )

        return new_operation

    def metrics(self):
        """
        Gather metrics from the LLM.
        """
        requested_values = [
            op._index for op in self.program.functions["main"].operations
        ]

        params = {
            "program": self.program.to_dict(),
            "requested_values": requested_values,
        }
        response = query_run_program(params)
        response.raise_for_status()

        data = [response[str(index)]["data"] for index in requested_values]

        return data


class Lambda:
    def __init__(self, builder: Builder, function: Function, output_value: Type):
        self.output_value = output_value
        self.builder = builder
        self.function = function

    def __call__(self, *args, **kwargs):
        input_value = self._get_input(*args, **kwargs)
        return self.builder.add_call(self.function, input_value, self.output_value)

    def _get_input(self, *args, **kwargs):
        # TODO: support more than one input LLM arg

        if len(args) > 0:
            return args[0]

        return next(iter(kwargs.values()))
