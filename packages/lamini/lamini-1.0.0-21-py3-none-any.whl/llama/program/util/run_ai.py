from typing import List, Union
import requests
import os
from llama.program.util.config import get_config, edit_config
import numpy as np
from sklearn.metrics.pairwise import cosine_similarity
import llama


def query_run_program(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/run_program")
    return resp


def query_submit_program_to_batch(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/submit_program")
    return resp


def query_check_llama_program_status(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/check_program_status")
    return resp


def query_get_llama_program_result(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/get_program_result")
    return resp


def query_cancel_llama_program(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/cancel_program")
    return resp


def query_submit_finetune_job(params):
    resp = powerml_send_query_to_url(params, "/v1/lamini/train")
    return resp


def query_check_training_job_status(params):
    resp = powerml_send_get_to_url(f"/v1/lamini/train/jobs/{params['job_id']}")
    return resp


def query_check_all_training_job_status():
    resp = powerml_send_get_to_url(f"/v1/lamini/train/jobs")
    return resp


def query_training_eval(params):
    resp = powerml_send_get_to_url(f"/v1/lamini/train/jobs/{params['job_id']}/eval")
    return resp


def query_cancel_training_job(params):
    resp = powerml_send_query_to_url(
        params, f"/v1/lamini/train/jobs/{params['job_id']}/cancel"
    )
    return resp


def query_cancel_all_training_jobs(params):
    resp = powerml_send_query_to_url(params, "/v1/lamini/train/jobs/cancel")
    return resp


def query_run_embedding(prompt: Union[str, List[str]], config={}):
    params = {"prompt": prompt}
    edit_config(config)
    resp = powerml_send_query_to_url(params, "/v1/inference/embedding")
    embeddings = resp.json()["embedding"]

    if isinstance(prompt, str):
        return np.reshape(embeddings, (1, -1))
    return [np.reshape(embedding, (1, -1)) for embedding in embeddings]


def query_get_models(params, config={}):
    edit_config(config)
    resp = powerml_send_query_to_url(params, "/v1/training/get_models")
    return resp.json()["models"]


def query_submit_data(params):
    resp = powerml_send_query_to_url(params, "/v1/llama/data")
    return resp


def query_clear_data(params):
    resp = powerml_send_query_to_url(params, "/v1/lamini/delete_data")
    return resp


def fuzzy_is_duplicate(embedding, reference_embeddings, threshold=0.99):
    if embedding is None:
        return True
    if not reference_embeddings:
        return False
    similarities = [
        cosine_similarity(embedding, reference_embedding)
        for reference_embedding in reference_embeddings
    ]

    most_similar_index = np.argmax(similarities)

    return np.round(similarities[most_similar_index], 15) >= threshold


def get_closest_embedding(embedding, reference_embeddings):
    if embedding is None:
        return None
    if not reference_embeddings:
        return None
    similarities = [
        cosine_similarity(embedding, reference_embedding)
        for reference_embedding in reference_embeddings
    ]

    most_similar_index = np.argmax(similarities)

    return reference_embeddings[most_similar_index]


def powerml_send_query_to_url(params, route):
    key, url = get_url_and_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
    }
    try:
        response = requests.post(
            url=url + route, headers=headers, json=params, timeout=200
        )
        response.raise_for_status()
    except requests.exceptions.Timeout:
        raise llama.error.APIError(f"Timeout error")
    except requests.exceptions.HTTPError as e:
        if response.status_code == 404:
            try:
                json_response = response.json()
            except Exception:
                json_response = {}
            raise llama.error.ModelNameError(
                json_response.get("detail", "ModelNameError")
            )
        if response.status_code == 429:
            try:
                json_response = response.json()
            except Exception:
                json_response = {}
            raise llama.error.RateLimitError(
                json_response.get("detail", "RateLimitError")
            )
        if response.status_code == 401:
            try:
                json_response = response.json()
            except Exception:
                json_response = {}
            raise llama.error.AuthenticationError(
                json_response.get("detail", "AuthenticationError")
            )
        if response.status_code == 400:
            try:
                json_response = response.json()
            except Exception:
                json_response = {}
            raise llama.error.UserError(json_response.get("detail", "UserError"))
        if response.status_code == 503:
            try:
                json_response = response.json()
            except Exception:
                json_response = {}
            raise llama.error.UnavailableResourceError(
                json_response.get("detail", "UnavailableResourceError")
            )
        if response.status_code != 200:
            try:
                description = response.json()
            except BaseException:
                description = response.status_code
            finally:
                if description == {"detail": ""}:
                    raise llama.error.APIError("500 Internal Server Error")
                raise llama.error.APIError(f"API error {description}")

    return response


def powerml_send_get_to_url(route):
    key, url = get_url_and_key()
    headers = {
        "Content-Type": "application/json",
        "Authorization": "Bearer " + key,
    }
    try:
        response = requests.get(url=url + route, headers=headers, timeout=200)
    except requests.exceptions.Timeout:
        raise llama.error.APIError(f"Timeout error")
    if response.status_code == 429:
        raise llama.error.RateLimitError(f"Rate limit error")
    if response.status_code == 401:
        raise llama.error.AuthenticationError(f"Check your api key")
    if response.status_code != 200:
        try:
            description = response.json()
        except BaseException:
            description = response.status_code
        finally:
            raise llama.error.APIError(f"API error {description}")
    return response


def get_url_and_key():
    cfg = get_config()
    environment = os.environ.get("LLAMA_ENVIRONMENT")
    if environment == "LOCAL":
        key = cfg.get("local.key", "test_token")
        url = cfg.get("local.url", "http://localhost:5001")
    elif environment == "STAGING":
        key = cfg.get("staging.key", "")
        url = cfg.get("staging.url", "https://api.staging.powerml.co")
    else:
        key = cfg.get("production.key", "")
        url = cfg.get("production.url", "https://api.powerml.co")
    return (key, url)


def get_ui_url():
    cfg = get_config()
    environment = os.environ.get("LLAMA_ENVIRONMENT")
    if environment == "LOCAL":
        url = cfg.get("local.url", "http://localhost:5001")
    elif environment == "STAGING":
        url = cfg.get("staging.url", "https://staging.powerml.co")
    else:
        if cfg.get("production.key", "") == "test_token":
            url = cfg.get("production.url", "http://localhost:5001")
        else:
            url = cfg.get("production.url", "https://app.lamini.ai")
    return url
