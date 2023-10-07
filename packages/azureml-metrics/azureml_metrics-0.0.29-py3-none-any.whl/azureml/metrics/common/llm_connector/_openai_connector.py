# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
import copy
import logging

from typing import List, Callable, Any
from azureml.metrics.common.exceptions import MissingDependencies

try:
    from openai import InvalidRequestError
    import openai
    import openai.error
    from tenacity import (
        before_sleep_log,
        retry,
        retry_if_exception_type,
        stop_after_attempt,
        wait_exponential,
    )

except ImportError:
    safe_message = "Relevant GPT Star metrics packages are not available. " \
                   "Please run pip install azureml-metrics[prompt-flow]"
    raise MissingDependencies(
        safe_message, safe_message=safe_message
    )

logger = logging.getLogger(__name__)


class OpenAIConnector:
    """class to handle connection with OpenAI, including retry, batching, parsing, etc."""
    def __init__(self,
                 openai_params: dict,
                 openai_api_batch_size: int = 20,
                 use_chat_completion_api: bool = None):
        self.openai_params = openai_params
        self.openai_api_batch_size = openai_api_batch_size
        self.use_chat_completion_api = use_chat_completion_api

    def get_openai_response_all_instances(self, prompts_list: list) -> List[List[str]]:
        """
        Get prediction from openai API.

        :param prompts_list: constructed prompts, this is a list of list of dictionary.
        :param openai_params: Dictionary containing credentials for openai API.
        """
        config_temperature = 0  # inorder to generate a deterministic result
        config_max_tokens = (
            1  # we need 1 token to produce the numerical output of score
        )

        results = []

        # updating the deployment_id if it's not set in openai_params
        if isinstance(self.openai_params, dict):
            if "deployment_id" not in self.openai_params.keys():
                self.openai_params["deployment_id"] = "gpt-35-turbo"
                logger.info("Using gpt-35-turbo for openai deployment_id as "
                            "deployment_id is not provided in openai_params")
            if "max_tokens" not in self.openai_params.keys():
                self.openai_params["max_tokens"] = config_max_tokens
            if "temperature" not in self.openai_params.keys():
                self.openai_params["temperature"] = config_temperature

            # retrieving the model name or deployment name when model is None
            model = self.openai_params.get("model", self.openai_params["deployment_id"])
        else:
            logger.warning("GPT related metrics need openai_params in a dictionary.")
            return results

        if self.use_chat_completion_api is None:
            if self.is_chat_completion_api(model):
                self.use_chat_completion_api = True
                # currently, batching is not supported in chat completion api.
                # so, setting the batch size to 1
                self.openai_api_batch_size = 1
            else:
                self.use_chat_completion_api = False
                # Note: We have observed that groundedness prompt is returning integer scores only
                # when we set "logit_bias" parameter for text-davinci family of models which use openai completion API.
                if "logit_bias" not in self.openai_params.keys():
                    self.openai_params["logit_bias"] = {16: 100, 17: 100, 18: 100, 19: 100, 20: 100}

        results = []
        for instance_prompts in prompts_list:
            instance_results = self.get_openai_response_single_instance_batch(instance_prompts,
                                                                              self.use_chat_completion_api)
            results.append(instance_results)
        return results

    def get_openai_response_single_instance_batch(self, instance_prompts: list,
                                                  use_chat_completion_api: bool) -> List[str]:
        results = []
        for index in range(0, len(instance_prompts), self.openai_api_batch_size):
            prompt_batch = list(instance_prompts[index: index + self.openai_api_batch_size])
            # setting the prompt in openai params
            self.openai_params["prompt"] = prompt_batch

            # start and end index of batch to be used in case of exception
            batch_start_index = index
            batch_end_index = min(len(instance_prompts), index + self.openai_api_batch_size)

            while True:
                try:
                    api_output = self.completion_with_retry()
                    break

                except InvalidRequestError:
                    logger.info("Content filter warning encountered. Going via single prompt "
                                "and skipping filtered results")
                    api_output = {"choices": []}

                    for row_index in range(batch_start_index, batch_end_index):
                        try:
                            cur_out = self.completion_with_retry()

                            if use_chat_completion_api:
                                predicted_result = cur_out["choices"][0]['message']['content']
                            else:
                                predicted_result = cur_out["choices"][0]["text"]

                            self.update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)

                        except InvalidRequestError as e:
                            predicted_result = e.__class__.__name__
                            logger.warning("Could not compute metric because of the following exception : " + str(e))
                            self.update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)
                    break

                except Exception as e:
                    api_output = {"choices": []}
                    for row_index in range(batch_start_index, batch_end_index):
                        predicted_result = e.__class__.__name__
                        logger.warning("Could not compute metric because of the following exception : " + str(e))
                        self.update_result(api_output, predicted_result, index, row_index, use_chat_completion_api)
                    break

            # Collect predictions from response
            for row in api_output["choices"]:
                if use_chat_completion_api:
                    result = row['message']['content']
                else:
                    result = row["text"]
                results.append(result)
        return results

    def is_chat_completion_api(self, model):
        """
        Check if we need openai chat completion or completion API for inference.

        :param model : model name to perform openai inference call.
        :return: True if we need to use chat-completion API.
        """
        # TODO : check if we need to update model_ids based on different endpoints.
        return model.startswith("gpt-35-turbo") or \
            model.startswith("gpt-3.5-turbo") or \
            model.startswith("gpt4") or \
            model.startswith("gpt-4")

    def update_result(self, api_output, predicted_result, index, row_index, use_chat_completion_api):
        """
        Updating result based on structure of completion or chat completion API.
        """
        if use_chat_completion_api:
            current_result = {
                "message": {"content": predicted_result, "role": "system"},
                "index": row_index - index
            }
        else:
            current_result = {"text": predicted_result, "index": row_index - index}
        api_output["choices"].append(current_result)

    def _create_retry_decorator(self) -> Callable[[Any], Any]:
        max_retries = 4
        min_seconds = 4
        max_seconds = 10
        # Wait 2^x * 1 second between each retry starting with
        # 4 seconds, then up to 10 seconds, then 10 seconds afterwards
        return retry(
            reraise=True,
            stop=stop_after_attempt(max_retries),
            wait=wait_exponential(multiplier=1, min=min_seconds, max=max_seconds),
            retry=(
                retry_if_exception_type(openai.error.Timeout)
                | retry_if_exception_type(openai.error.APIError)
                | retry_if_exception_type(openai.error.APIConnectionError)
                | retry_if_exception_type(openai.error.RateLimitError)
                | retry_if_exception_type(openai.error.ServiceUnavailableError)
            ),
            before_sleep=before_sleep_log(logger, logging.WARNING),
        )

    def completion_with_retry(self) -> Any:
        """Use tenacity to retry the completion call.
        Copied from:
        https://github.com/hwchase17/langchain/blob/42df78d3964170bab39d445aa2827dea10a312a7/langchain/llms/openai.py#L98
        """
        retry_decorator = self._create_retry_decorator()

        @retry_decorator
        def _completion_with_retry() -> Any:
            # retrieving deployment_id if model is not present in openai parameters
            model = self.openai_params.get("model", self.openai_params["deployment_id"])

            if model.startswith("gpt-35-turbo") or model.startswith("gpt-3.5-turbo") \
                    or model.startswith("gpt4") or model.startswith("gpt-4"):
                openai_params_chat_api = copy.deepcopy(self.openai_params)
                openai_params_chat_api['messages'] = openai_params_chat_api['prompt'][0]

                # deleting the prompt as we are adding messages
                del openai_params_chat_api['prompt']

                if 'best_of' in openai_params_chat_api:
                    del openai_params_chat_api['best_of']

                return openai.ChatCompletion.create(**openai_params_chat_api)
            else:
                messages_prompt_list = self.openai_params.get("prompt", None)
                if messages_prompt_list is not None and isinstance(messages_prompt_list, list):
                    prompt_text = [message_prompt[1]["content"] for message_prompt in messages_prompt_list]
                    self.openai_params["prompt"] = prompt_text

                return openai.Completion.create(**self.openai_params)

        return _completion_with_retry()
