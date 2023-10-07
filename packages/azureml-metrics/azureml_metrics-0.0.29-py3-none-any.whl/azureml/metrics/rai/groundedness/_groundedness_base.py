# ---------------------------------------------------------
# Copyright (c) Microsoft Corporation. All rights reserved.
# ---------------------------------------------------------
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#     http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.


"""Definitions for Groundedness metrics."""
import logging
from abc import abstractmethod
import numpy as np
from typing import Any, List, Optional, Dict
from azureml.metrics.common._metric_base import Metric
from azureml.metrics.common.exceptions import MissingDependencies
from azureml.metrics import constants

logger = logging.getLogger(__name__)


class GroundednessBase(Metric):
    """GPTGroundedness metric for comparison of generated content vs. context"""

    def __init__(self,
                 generated_contents: List[str],
                 tokenizer: Any,
                 contexts: List[str],
                 openai_params: dict,
                 regexes_to_ignore: Optional[List[str]] = None,
                 ignore_case: bool = False,
                 ignore_punctuation: bool = False,
                 ignore_numbers: bool = False,
                 lang: Optional[str] = "en",
                 openai_api_batch_size: Optional[int] = 20,
                 use_chat_completion_api: Optional[bool] = None,
                 ) -> None:
        """
        :param generated_contents: list of generated contents to evaluate groundedness
        :param tokenizer: function that takes input a string, and returns a list of tokens
        :params regexes_to_ignore: List of string regular expressions to ignore
        :params ignore_case: Boolean to indicate whether to ignore case
        :params ignore_punctuation: Boolean to indicate whether to ignore punctuation
        :params ignore_numbers: Boolean to indicate whether to ignore numbers
        :param contexts: list of contexts against which to evaluate groundedness
        :param openai_params: Dictionary contating credentials for openai API.
        :params lang: String value to indicate the language of provided data.
        :param openai_api_batch_size: number of prompts to be batched in one API call.
        :param use_chat_completion_api: boolean flag to choose between openAI completion vs chat completion API.
        """
        try:
            from azureml.metrics.common.llm_connector._openai_connector import OpenAIConnector
        except ImportError:
            safe_message = "Relevant GPT Star metrics packages are not available. " \
                           "Please run pip install azureml-metrics[prompt-flow]"
            raise MissingDependencies(
                safe_message, safe_message=safe_message
            )
        self.tokenizer = tokenizer
        self.regexes_to_ignore = regexes_to_ignore
        self.ignore_case = ignore_case
        self.ignore_punctuation = ignore_punctuation
        self.ignore_numbers = ignore_numbers
        self.lang = lang
        self.generated_contents = generated_contents
        self.contexts = contexts
        self.openai_api_batch_size = openai_api_batch_size
        self.openai_params = openai_params
        self.use_chat_completion_api = use_chat_completion_api
        self.openai_connector = OpenAIConnector(openai_params, openai_api_batch_size,
                                                use_chat_completion_api)
        super().__init__()

    @abstractmethod
    def construct_user_prompts(self, context: str, gen_content: str) -> List[str]:
        ...

    def get_system_prompt(self) -> str:
        """this is a default system prompt, can be overwritten by child classes"""
        system_prompt = "You are an AI assistant. You will be given the definition of an " \
            "evaluation metric for assessing the quality of an answer in a " \
            "question-answering task. Your job is to compute an accurate evaluation " \
            "score using the provided evaluation metric."
        return system_prompt

    # in the future child class can overwrite post process function
    def post_process(self, raw_results) -> List[str]:
        results = []
        for result in raw_results:
            results.append(result[0].strip().lower())
        return results

    def check_kwargs(self, metric_name: str) -> Any:
        if metric_name == constants.Metric.GPTGroundedness:
            if self.openai_params is None:
                logger.error("OpenAI params not provided.")
                return "nan"
            if self.generated_contents is None:
                logger.error("Generated contents not provided.")
                return "nan"
            if self.contexts is None:
                logger.error("Contexts not provided.")
                return "nan"

    def compute(self) -> Any:
        """compute the score for GPTGroundedness metric"""
        if self.check_kwargs(constants.Metric.GPTGroundedness) == "nan":
            return ["not-applicable" for _ in range(len(self.y_pred))]

        prompt_list = []

        for context, generated_content in zip(self.contexts, self.generated_contents):
            prompts = self.construct_full_prompts(self.construct_user_prompts(context, generated_content))
            prompt_list.append(prompts)

        results_raw = self.openai_connector.get_openai_response_all_instances(prompt_list)
        logger.debug("gpt groundedness results : {}".format(results_raw))

        # post process
        results = self.post_process(results_raw)
        return results

    def get_formatting_reminder(self) -> str:
        reminder = "Reminder: The return values for each task should be correctly formatted as an integer " \
            "between 1 and 5. Do not repeat the context and question.\n"
        return reminder

    def construct_full_prompts(self, user_prompt_list) -> List[Dict[str, str]]:
        """ this can be overwritten by child classes that want more flexibility,
        e.g. with different names for few shot examples"""
        messages = [{"role": "system", "content": self.get_system_prompt()}]
        result = []
        for user_prompt in user_prompt_list:
            result.append(messages + [{"role": "user", "content": user_prompt}])
        return result

    @staticmethod
    def aggregate(
            scores: List[Any]
    ) -> float:
        """
        Fold several scores from a computed metric together. For now,
        it is a list of list of strings, but the inside list has len 1

        :param scores: List of List of str, response from openai
        :return: Aggregated score.
        """
        int_scores = []
        for score in scores:
            try:
                int_scores.append(int(score[0]))
            except ValueError:
                int_scores.append(np.nan)

        if np.isnan(int_scores).sum() == len(int_scores):
            logger.error("Score aggregation failed with all non-integer scores")
            return float(np.nan)
        return float(np.nanmean(int_scores))
