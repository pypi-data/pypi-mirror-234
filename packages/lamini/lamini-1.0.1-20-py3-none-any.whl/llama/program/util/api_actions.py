from typing import List

from llama.program.util.run_ai import (
    query_run_program,
    query_submit_program_to_batch,
    query_check_llama_program_status,
    query_get_llama_program_result,
    query_cancel_llama_program,
    query_submit_finetune_job,
    query_submit_data,
    query_clear_data,
    query_check_training_job_status,
    query_check_all_training_job_status,
    query_cancel_training_job,
    query_cancel_all_training_jobs,
    query_training_eval,
)
from llama.program.value import Value


def gen_queue_batch(values: List[Value]):
    # Assume that all values have the same program
    program = values[0]._function.program.to_dict()
    params = {
        "program": program,
        "requested_values": [v._index for v in values],
    }
    response = query_submit_program_to_batch(params)
    response.raise_for_status()
    return response.json()


def gen_submit_training_job(
    id,
    model_name,
    data,
    prompt_key,
    enable_peft,
    finetune_args,
    peft_args,
    is_public,
    use_cached_model,
    prompt_templates,
):
    assert isinstance(id, str)
    assert isinstance(model_name, str)
    # Assume that all values have the same program
    params = {
        "id": id,
        "model_name": model_name,
        "data": data,
        "prompt_key": prompt_key,
        "enable_peft": enable_peft,
        "finetune_args": finetune_args,
        "peft_args": peft_args,
        "prompt_templates": prompt_templates,
        "is_public": is_public,
        "use_cached_model": use_cached_model,
    }
    response = query_submit_finetune_job(params)
    response.raise_for_status()
    return response.json()


def gen_training_job_status(job_id: int):
    if not isinstance(job_id, int):
        try:
            job_id = int(job_id)
        except:
            raise Exception(f"job_id must be an integer, but instead got {job_id}")
    assert isinstance(job_id, int)
    params = {
        "job_id": job_id,
    }
    response = query_check_training_job_status(params)
    response.raise_for_status()
    return response.json()


def gen_all_training_job_status():
    response = query_check_all_training_job_status()
    response.raise_for_status()
    return response.json()


def gen_cancel_training_job(job_id: int):
    assert isinstance(job_id, int)
    params = {
        "job_id": job_id,
    }
    response = query_cancel_training_job(params)
    response.raise_for_status()
    return response.json()


def gen_cancel_training_jobs():
    params = {}
    response = query_cancel_all_training_jobs(params)
    response.raise_for_status()
    return response.json()


def gen_inference_job_status(job_id: str):
    # Assume that all values have the same program
    assert isinstance(job_id, str)
    params = {
        "job_id": job_id,
    }
    response = query_check_llama_program_status(params)
    response.raise_for_status()
    return response.json()


def gen_training_eval(job_id: int):
    assert isinstance(job_id, int)
    params = {
        "job_id": job_id,
    }
    response = query_training_eval(params)
    response.raise_for_status()
    return response.json()


def gen_inference_job_results(job_id: str, output_type=None):
    # Assume that all values have the same program
    assert isinstance(job_id, str)
    params = {
        "job_id": job_id,
    }
    response = query_get_llama_program_result(params)
    response.raise_for_status()
    response = response.json()
    if "Error" in response:
        return response
    if output_type is None:
        return response
    outputs = []
    for key, val in response.items():
        data = val["data"]
        for d in data:
            obj = output_type.parse_obj(d)
            outputs.append(obj)
    if len(outputs) == 1:
        return outputs[0]
    return outputs


def gen_cancel_job(job_id: str):
    # Assume that all values have the same program
    assert isinstance(job_id, str)
    params = {
        "job_id": job_id,
    }
    response = query_cancel_llama_program(params)
    response.raise_for_status()
    return response.json()


def gen_submit_data(program, id):
    program = program.to_dict()
    assert isinstance(id, str)
    params = {
        "id": id,
        "data": program["examples"],
    }
    response = query_submit_data(params)
    response.raise_for_status()
    return response.json()


def gen_clear_data(id):
    assert isinstance(id, str)
    params = {
        "id": id,
    }
    response = query_clear_data(params)
    response.raise_for_status()
    return response.json()


def gen_multiple_values(values: List[Value]):
    # Assume that all values have the same program
    program = values[0]._function.program.to_dict()
    params = {
        "program": program,
        "requested_values": [v._index for v in values],
    }
    response = query_run_program(params)
    response.raise_for_status()
    for i, v in enumerate(values):
        index = v._index
        response_val = response.json()[str(index)]
        if isinstance(response_val["data"], list):
            v._data = []
            for d in response_val["data"]:
                v._data.append(v._type.parse_obj(d))
        else:
            v._data = v._type.parse_obj(response_val["data"])
    # Update cache once
    values[0]._function.program.builder.value_cache.update(response.json())
    return [value._data for value in values]


def gen_value(value: Value):
    value._compute_value()
    return value._data
