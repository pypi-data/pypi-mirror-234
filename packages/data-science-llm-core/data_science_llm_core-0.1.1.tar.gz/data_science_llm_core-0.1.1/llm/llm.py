"""LLM based functionalities and prompt example."""
import asyncio
import json
import os

import backoff
import openai
from dotenv import dotenv_values
from tqdm import asyncio as tqdm_asyncio

from llm.io import logger


def authorize_openai(params):
    """Authorize openai from environment variables and params."""
    secret_path = f'{params["folder_secrets"]}/{params["env_file"]}'
    if os.path.exists(secret_path):
        env_vars = dotenv_values(secret_path)
        os.environ.update(env_vars)
    else:
        # Return an error if the file doesn't exist
        logger.warning(f"File {secret_path} does not exist...")

    openai.api_key = os.environ["OPENAI_API_KEY"]


# The function to make network calls
# Decorator for the network call with backoff functionality
# Backoff is a library that provides function decorators and
# context managers that enable easy usage of backoff/retry
# strategies when calling unstable remote resources.
# It retries the function if it fails with a aforementioned errors
# below. with maximum of max_tries times with a factor of factor every time.
@backoff.on_exception(
    backoff.expo,
    (
        openai.error.RateLimitError,
        openai.error.Timeout,
        openai.error.ServiceUnavailableError,
        openai.error.TryAgain,
        openai.error.APIError,
        openai.error.APIConnectionError,
        openai.error.OpenAIError,
        json.JSONDecodeError,
    ),
    max_tries=20,
    max_time=30,
    factor=1.41421356237304486532,  # I literally hand calculated this when I was 12 :)
)
async def query_llm(function, input_dict):
    """Encapsulate function with backoff capabilities."""
    return await function(input_dict=input_dict)


async def parallel_requests(requests, func):
    """Make all requests in parallel over function func."""
    # Temporary function to make the parallel requests with index i
    # so that we can sort the random order afterwards
    async def temp_function(req, i, func):
        res = await query_llm(func, input_text=req)
        return i, res

    # Initialize the tqdm progress bar with the total number of tasks
    tasks = []
    for i, req in enumerate(requests):
        # This executes the prompts but does NOT waits for their output
        # so everything is in parallel
        tasks += [asyncio.create_task(temp_function(req, i, func))]

    results = []
    # This part is the waiting for everything to get executed in parallel
    # and arbitrary order. We use tqdm to show the progress bar.
    with tqdm_asyncio.tqdm(total=len(tasks), desc="Parallel Query Execution:") as pbar:
        for coro in asyncio.as_completed(tasks):
            result = await coro
            results.append(result)
            pbar.update(1)

    # This part sorts the outputs with the index that temp function provided
    # so that we can get the results in the same order as the requests.
    # and drop the index afterwards.
    results = sorted(results, key=lambda x: x[0])
    results = [i for _, i in results]
    return results
